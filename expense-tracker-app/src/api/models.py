from sqlalchemy import(Column, CHAR, TEXT, Integer, BigInteger, Numeric, Date, DateTime, LargeBinary, ForeignKey, CheckConstraint, text)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(CHAR(8), primary_key=True)
    full_name = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False, unique=True)
    pin_hash = Column(TEXT, nullable=False)
    failed_attempts = Column(Integer, nullable=False, server_default=text("0"))
    locked_until = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    __table_args__ = (
        CheckConstraint("failed_attempts >= 0", name="users_failed_attempts_check"),
        CheckConstraint("user_id ~ '^[0-9]{8}$'", name="users_user_id_format")
    )

class Expenses(Base):
    __tablename__ = 'expenses'

    expense_id = Column(BigInteger, primary_key=True, autoincrement=True)  
    user_id = Column(CHAR(8), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category = Column(TEXT, nullable=False)
    subcategory = Column(TEXT, nullable=False) 
    description = Column(TEXT, nullable=False)
    amount = Column(Numeric(14,2), nullable=False) 
    food_cost = Column(Numeric(14,2))
    delivery_fee = Column(Numeric(14,2))
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    spent_on = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    receipt_image = Column(LargeBinary)
    recipient = Column(TEXT)
    settled_by = Column(BigInteger, ForeignKey("expenses.expense_id", ondelete="SET NULL"))

    __table_args__ = (
        CheckConstraint("amount >= 0", name="expenses_amount_check"),
    )
