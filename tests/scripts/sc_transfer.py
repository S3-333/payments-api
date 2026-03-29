# Script manual: ejecuta una transferencia por IDs (requiere cuentas existentes).

from decimal import Decimal

from src.application.use_cases.transfer_money import TransferMoneyUseCase
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.repositories.account_repository_impl import AccountRepositoryImpl
from src.infrastructure.database.repositories.transfer_ledger_repository_impl import (
    TransferLedgerRepositoryImpl,
)


def main() -> None:
    db = SessionLocal()
    try:
        uc = TransferMoneyUseCase(AccountRepositoryImpl(), TransferLedgerRepositoryImpl())
        uc.execute(db, 2, 99, Decimal("30.00"))
        print("Transferencia ejecutada (revisa IDs en tu base; 2 y 99 deben existir).")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()


if __name__ == "__main__":
    main()
