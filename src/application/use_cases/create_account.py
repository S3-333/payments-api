# Caso de uso: crear cuenta. Orquesta validaciones de dominio y persistencia.
# Aquí es el ÚNICO sitio que hace commit/rollback para esta operación (una transacción clara).

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from src.domain.exceptions import InvalidInitialBalanceError
from src.domain.repositories.account_repository import AccountRepository
from src.domain.value_objects.money import Money


class CreateAccountUseCase:
    """
    Aplica la regla de negocio: saldo inicial no negativo (lo garantiza Money),
    luego delega la creación al repositorio.

    Por qué una clase: agrupa dependencias (repositorio) y facilita inyección en tests y FastAPI.
    """

    def __init__(self, accounts: AccountRepository) -> None:
        self._accounts = accounts

    def execute(self, session: Session, owner: str, initial_balance: Decimal):
        """
        Crea la cuenta en una sola transacción SQL.

        - session: sesión SQLAlchemy abierta por la capa de presentación (Depends).
        - commit ocurre aquí si todo va bien; rollback si hay error.
        """
        try:
            # Money centraliza formato y rechazo de valores negativos.
            money = Money.from_decimal(initial_balance)
        except ValueError as e:
            raise InvalidInitialBalanceError("El balance inicial no puede ser negativo") from e

        try:
            account = self._accounts.create(session, owner, money)
            session.commit()
            return account
        except Exception:
            session.rollback()
            raise
