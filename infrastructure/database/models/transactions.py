from typing import Optional

from sqlalchemy import DECIMAL, ForeignKey, Integer, String
from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class Transaction(Base, TimestampMixin, TableNameMixin):
    tx_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    invoice_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[float] = mapped_column(DECIMAL(16, 8))
    status: Mapped[str] = mapped_column(String(16))
    hash: Mapped[str] = mapped_column(String(64))
    asset: Mapped[Optional[str]] = mapped_column(String(16))
    bot_invoice_url: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    paid_at: Mapped[Optional[str]] = mapped_column(String(255))
    expiration_date: Mapped[Optional[str]] = mapped_column(String(255))
    comment: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self):
        return (
            f"<Transaction {self.tx_id} {self.invoice_id} {self.amount} {self.status}"
        )
