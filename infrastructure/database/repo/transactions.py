from typing import Optional

from aiocryptopay.models.invoice import Invoice
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Transaction
from infrastructure.database.repo.base import BaseRepo


class TransactionRepo(BaseRepo):
    async def create_transaction(self, user_id: int, invoice: Invoice):
        statement = insert(Transaction).values(
            user_id=user_id,
            invoice_id=invoice.invoice_id,
            amount=invoice.amount,
            status=invoice.status,
            hash=invoice.hash,
            asset=invoice.asset,
            bot_invoice_url=invoice.bot_invoice_url,
            description=invoice.description,
            paid_at=invoice.paid_at,
            expiration_date=invoice.expiration_date,
            comment=invoice.comment,
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def update_transaction(self, invoice: Invoice):
        statement = (
            update(Transaction)
            .where(Transaction.invoice_id == invoice.invoice_id)
            .values(
                status=invoice.status,
                paid_at=invoice.paid_at,
                comment=invoice.comment,
            )
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_user_for_invoice(self, invoice_id: int) -> Optional[int]:
        statement = select(Transaction.user_id).where(
            Transaction.invoice_id == invoice_id
        )
        return await self.session.scalar(statement)

    # not applicable for our use case
    # async def get_user_balance(self, user_id: int) -> Optional[float]:
    #     statement = select(func.sum(Transaction.amount)).where(
    #         Transaction.user_id == user_id,
    #         Transaction.status == "paid",
    #     )

    #     return await self.session.scalar(statement)
