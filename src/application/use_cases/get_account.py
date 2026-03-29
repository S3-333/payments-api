# Caso de uso simple: consultar una cuenta por id (solo lectura, sin commit necesario).

from __future__ import annotations

from sqlalchemy.orm import Session

from src.domain.entities.account import Account
from src.domain.exceptions import AccountNotFoundError
from src.domain.repositories.account_repository import AccountRepository


class GetAccountUseCase:
    """Encapsula la consulta para que la ruta HTTP no llame al repositorio directamente."""

    def __init__(self, accounts: AccountRepository) -> None:
        self._accounts = accounts

    def execute(self, session: Session, account_id: int) -> Account:
        account = self._accounts.get_by_id(session, account_id, for_update=False)
        if account is None:
            raise AccountNotFoundError("Cuenta no encontrada")
        return account
