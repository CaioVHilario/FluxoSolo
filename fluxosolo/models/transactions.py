from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    transactions: Mapped[list[Transaction]] = relationship(
        init=False,
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


@mapped_as_dataclass(table_registry)
class Category:
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    transactions: Mapped[list[Transaction]] = relationship(
        init=False, back_populates="category", lazy="selectin"
    )


@mapped_as_dataclass(table_registry)
class TransactionType:
    __tablename__ = "transactions_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    transactions: Mapped[list[Transaction]] = relationship(
        init=False, back_populates="transaction_type", lazy="selectin"
    )


@mapped_as_dataclass(table_registry)
class Bank:
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    transactions: Mapped[list[Transaction]] = relationship(
        init=False, back_populates="bank", lazy="selectin"
    )


@mapped_as_dataclass(table_registry)
class Transaction:
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    date: Mapped[datetime]
    value: Mapped[float] = mapped_column(Numeric(10, 2))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    transaction_type_id: Mapped[int] = mapped_column(
        ForeignKey("transactions_type.id")
    )
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))

    details: Mapped[str | None] = mapped_column(default=None)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(
        init=False, back_populates="transactions"
    )
    category: Mapped[Category] = relationship(
        init=False, back_populates="transactions"
    )
    transaction_type: Mapped[TransactionType] = relationship(
        init=False, back_populates="transactions"
    )
    bank: Mapped[Bank] = relationship(
        init=False, back_populates="transactions"
    )
