# Integración: mismo flujo que producción (repositorios reales + SQLAlchemy) contra SQLite en memoria.

from decimal import Decimal

from src.application.use_cases.transfer_money import TransferMoneyUseCase
from src.infrastructure.database.models.account_model import AccountORM
from src.infrastructure.database.repositories.account_repository_impl import AccountRepositoryImpl
from src.infrastructure.database.repositories.transfer_ledger_repository_impl import (
    TransferLedgerRepositoryImpl,
)


def test_transfer_real_db(db_session) -> None:
    repo = AccountRepositoryImpl()
    ledger = TransferLedgerRepositoryImpl()

    acc1 = AccountORM(owner="Juan", balance=Decimal("100.00"))
    acc2 = AccountORM(owner="Ana", balance=Decimal("50.00"))
    db_session.add(acc1)
    db_session.add(acc2)
    db_session.commit()
    db_session.refresh(acc1)
    db_session.refresh(acc2)

    uc = TransferMoneyUseCase(repo, ledger)
    uc.execute(db_session, acc1.id, acc2.id, Decimal("30.00"))

    db_session.expire_all()
    updated_acc1 = db_session.get(AccountORM, acc1.id)
    updated_acc2 = db_session.get(AccountORM, acc2.id)

    assert updated_acc1 is not None and updated_acc2 is not None
    assert updated_acc1.balance == Decimal("70.00")
    assert updated_acc2.balance == Decimal("80.00")
