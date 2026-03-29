# =============================================================================
# Dependencias de FastAPI (inyección):
#
# FastAPI llama a estas funciones cuando una ruta declara Depends(...).
# Así la ruta recibe ya lista la sesión de BD y el caso de uso, sin hacer "new" a mano.
#
# Cadena típica:
#   get_transfer_money_use_case
#     -> pide AccountRepositoryImpl y TransferLedgerRepositoryImpl
#     -> construye TransferMoneyUseCase(accounts, ledger)
# =============================================================================

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.use_cases.create_account import CreateAccountUseCase
from src.application.use_cases.get_account import GetAccountUseCase
from src.application.use_cases.transfer_money import TransferMoneyUseCase
from src.domain.repositories.account_repository import AccountRepository
from src.domain.repositories.transfer_ledger_repository import TransferLedgerRepository
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.repositories.account_repository_impl import AccountRepositoryImpl
from src.infrastructure.database.repositories.transfer_ledger_repository_impl import (
    TransferLedgerRepositoryImpl,
)


def get_db() -> Generator[Session, None, None]:
    """
    Una sesión de SQLAlchemy por petición HTTP.

    - yield: FastAPI ejecuta la ruta con `db` y luego continúa después del yield
    - finally close: siempre cierra la sesión (aunque la ruta falle)
    El commit lo hace el caso de uso, no esta función (transacción explícita).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_account_repository() -> AccountRepository:
    # Tipo de retorno es la interfaz (dominio); la instancia real es la de infraestructura.
    return AccountRepositoryImpl()


def get_transfer_ledger_repository() -> TransferLedgerRepository:
    return TransferLedgerRepositoryImpl()


def get_create_account_use_case(
    repo: AccountRepository = Depends(get_account_repository),
) -> CreateAccountUseCase:
    # Depends resuelve el repositorio y lo pasa al constructor del caso de uso.
    return CreateAccountUseCase(repo)


def get_get_account_use_case(
    repo: AccountRepository = Depends(get_account_repository),
) -> GetAccountUseCase:
    return GetAccountUseCase(repo)


def get_transfer_money_use_case(
    accounts: AccountRepository = Depends(get_account_repository),
    ledger: TransferLedgerRepository = Depends(get_transfer_ledger_repository),
) -> TransferMoneyUseCase:
    # La transferencia necesita dos puertos: cuentas + libro de movimientos.
    return TransferMoneyUseCase(accounts, ledger)
