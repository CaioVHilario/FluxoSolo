from datetime import datetime

from sqlalchemy import func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, mapped_as_dataclass, registry

table_registry = registry()

@mapped_as_dataclass(table_registry)
class Transaction:
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    date: Mapped[datetime]
    transaction: Mapped[str]
    value: Mapped[float] = mapped_column(Numeric(10, 2))
    bank: Mapped[str]
    details: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
