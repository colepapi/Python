from pydantic import(BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator)
from typing import Annotated
from decimal import Decimal
from datetime import date, datetime

UserID = Annotated[str, StringConstraints(pattern=r"^[0-9]{8}$")]
SixDigitPIN = Annotated[str, StringConstraints(pattern=r"^[0-9]{6}$")]
Money = Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=2)]

weak_pins = {"000000", "111111", "123456", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999", "654321"}


class UserBase(BaseModel):
    full_name: str = Field(min_length=1)
    email: EmailStr

class UserCreate(UserBase):
    pin: SixDigitPIN

    @field_validator("pin")

    @classmethod
    def reject_weak_pin(cls, value: str) -> str:
        if value in weak_pins:
            raise ValueError("This PIN is too easy to guess. Please choose a different six-digit PIN.")
        return value

class UserLogin(BaseModel):
    user_id: Annotated[str, StringConstraints(pattern=r"^[0-9]{8}$")]
    pin: SixDigitPIN

class UserRead(UserBase):
    user_id: UserID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExpenseCreate(BaseModel):
    category: str = Field(min_length=1)
    subcategory: str = Field(min_length=1)
    description: str = Field(min_length=1)
    amount: Money
    food_cost: Money | None = None
    delivery_fee: Money | None = None
    spent_on: date | None = None
    recipient: str | None = Field(default=None)

class ExpenseRead(BaseModel):
    expense_id: int
    user_id: UserID
    category: str
    subcategory: str
    description: str
    amount: Money
    food_cost: Money | None = None
    delivery_fee: Money | None = None
    recorded_at: datetime
    spent_on: date
    recipient: str | None = None
    settled_by: int | None = None

    model_config = ConfigDict(from_attributes=True)