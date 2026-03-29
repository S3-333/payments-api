# Persistencia del historial de transferencias (tabla transfer_records).

from sqlalchemy.orm import Session

from src.domain.repositories.transfer_ledger_repository import TransferLedgerRepository
from src.domain.value_objects.money import Money
from src.infrastructure.database.models.transaction_model import TransferRecordORM


class TransferLedgerRepositoryImpl(TransferLedgerRepository):
    def append_transfer(
        self,
        session: Session,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
    ) -> None:
        row = TransferRecordORM(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount.amount,
        )
        session.add(row)
