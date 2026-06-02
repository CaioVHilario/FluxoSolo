from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int


class CategoryPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class BankPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TransactionTypePublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TransactionsPublic(BaseModel):
    id: int
    date: datetime
    value: float
    details: str | None

    category: CategoryPublic
    bank: BankPublic
    transaction_type: TransactionTypePublic
    model_config = ConfigDict(from_attributes=True)


class TransactionsList(BaseModel):
    transactions: list[TransactionsPublic]


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=100)


class FilterTransactions(FilterPage):
    year: int | None = Field(default=None, description='Ex: 2026')
    month: int | None = Field(
        default=None, ge=1, le=12, description='Mẽs 1 a 12'
    )
