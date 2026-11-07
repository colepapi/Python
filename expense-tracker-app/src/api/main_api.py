from fastapi import(FastAPI, HTTPException, Depends, status)
from typing import Annotated
from src.database import get_session_factory
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from math import ceil
from fastapi.security import(HTTPAuthorizationCredentials, HTTPBearer)
from . import models, schemas

import os
import secrets
import jwt

app = FastAPI()
SessionLocal = get_session_factory()

MAX_ATTEMPTS = 3
LOCKOUT_TIME = 50 

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is not configured.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 420

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_pin(pin: str) -> str:
    return pwd_context.hash(pin)

def verify_pin(entered_pin: str, stored_hash: str) -> bool:
    return pwd_context.verify(entered_pin, stored_hash)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_access_token(user_id: str) -> str:
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": user_id,
        "exp": expires_at
        }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)], db: db_dependency) -> models.Users:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token is required.", headers={"WWW-Authenticate": "Bearer"})

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]})

        user_id = payload.get("sub")

        if not isinstance(user_id, str):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.", headers={"WWW-Authenticate": "Bearer"})

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token.", headers={"WWW-Authenticate": "Bearer"})

    current_user = (db.query(models.Users).filter(models.Users.user_id == user_id).first())

    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The account associated with this token no longer exists.", headers={"WWW-Authenticate": "Bearer"})
    return current_user

def generate_unique_user_id(db: Session) -> str:
    for _ in range(20):
        candidate = str(secrets.randbelow(90_000_000) + 10_000_000)

        existing_user = (db.query(models.Users).filter(models.Users.user_id == candidate).first())
        if existing_user is None:
            return candidate

    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Could not allocate a user ID. Please try again.")


# CREATING ENDPOINTS FOR USER REGISTRATION
# POST
@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(person: schemas.UserCreate, db: db_dependency):
    existing_email = (db.query(models.Users).filter(models.Users.email == str(person.email)).first())
    if existing_email is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    # Generate the ID and hash the submitted PIN.
    user_id = generate_unique_user_id(db)
    pin_hash = hash_pin(person.pin)

    db_person = models.Users(user_id=user_id, full_name=person.full_name, email=str(person.email), pin_hash=pin_hash)
    db.add(db_person)
    try:
        db.commit()
        db.refresh(db_person)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The Email or Generated User ID already exists. Please retry registration.")

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration could not be completed.")

    return db_person
        

# GET
@app.get("/users/me", response_model=schemas.UserRead)
async def get_user(current_user: Annotated[models.Users, Depends(get_current_user)]):
    return current_user


# LOGIN ENDPOINT
@app.post("/login")
async def login(credentials:schemas.UserLogin, db: db_dependency):
    existing_user = (db.query(models.Users).filter(models.Users.user_id == credentials.user_id).with_for_update().first())
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID or PIN.", headers={"WWW-Authenticate": "Bearer"})

    now = datetime.now(timezone.utc)

    if (existing_user.failed_attempts >= MAX_ATTEMPTS and existing_user.locked_until is None):
        existing_user.locked_until = (now + timedelta(seconds=LOCKOUT_TIME))

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=(
                f"Too many failed attempts. Account locked for {LOCKOUT_TIME} seconds."))

    # Check an active lockout BEFORE checking the PIN.
    if (existing_user.locked_until is not None and now < existing_user.locked_until):
        remaining_seconds = max(1, ceil((existing_user.locked_until - now).total_seconds()))

        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=(
                f"Account Locked. Try again in {remaining_seconds} seconds."))

    # If the previous lockout has expired, reset the previous attempt count before processing this login.
    if (existing_user.locked_until is not None and now >= existing_user.locked_until):
        existing_user.failed_attempts = 0
        existing_user.locked_until = None

    # Verify the entered PIN against the stored hash.
    pin_is_valid = verify_pin(credentials.pin, existing_user.pin_hash)

    # Handle an incorrect PIN.
    if not pin_is_valid:
        existing_user.failed_attempts += 1
        attempts_remaining = max(0, MAX_ATTEMPTS - existing_user.failed_attempts)

        # The third failed attempt triggers the lockout.
        if existing_user.failed_attempts >= MAX_ATTEMPTS:
            existing_user.locked_until = (now + timedelta(seconds=LOCKOUT_TIME))

            db.commit()

            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=(
                    f"Too many failed attempts. Account locked for {LOCKOUT_TIME} seconds."))

        # Persist the failed-attempt count.
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                f"Invalid user ID or PIN. {attempts_remaining} attempt(s) remaining."), headers={"WWW-Authenticate": "Bearer"})

    # The PIN is correct. Reset the attempt counter and clear any expired lockout.
    existing_user.failed_attempts = 0
    existing_user.locked_until = None

    db.commit()

    # Issue a token only after successful authentication.
    access_token = create_access_token(existing_user.user_id)

    return {
        "token_type": "Bearer token",
        "access_token": access_token
    }


# CREATING ENDPOINTS FOR EXPENSES
# GET
@app.get("/expenses", response_model=list[schemas.ExpenseRead])
async def get_expenses(db: db_dependency, current_user: Annotated[models.Users, Depends(get_current_user)]):
    result = (db.query(models.Expenses).filter(models.Expenses.user_id == current_user.user_id).order_by(models.Expenses.recorded_at.desc()).all())

    return result

@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseRead)
async def get_expense(expense_id: int, db: db_dependency, current_user: Annotated[models.Users, Depends(get_current_user)]):
    result = (db.query(models.Expenses).filter(models.Expenses.expense_id == expense_id, models.Expenses.user_id == current_user.user_id).first())

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense cannot be found.")

    return result


@app.post("/expenses", response_model=schemas.ExpenseRead, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: schemas.ExpenseCreate, db: db_dependency, current_user: Annotated[models.Users, Depends(get_current_user)]):

    # Exclude omitted and None fields so database defaults can apply to fields such as spent_on and recorded_at.
    expense_data = expense.model_dump(exclude_unset=True, exclude_none=True)

    # The owner comes from the authenticated token never from a user_id submitted by the client.
    db_expense = models.Expenses(user_id=current_user.user_id, **expense_data)
    db.add(db_expense)

    try:
        db.commit()
        db.refresh(db_expense)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=("The expense could not be saved because one or more fields violate a database constraint."))
    
    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The expense could not be saved.")

    return db_expense
