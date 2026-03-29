# Implementación concreta del repositorio de cuentas usando SQLAlchemy 2.x (select + Session).

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.account import Account
from src.domain.exceptions import AccountNotFoundError
from src.domain.repositories.account_repository import AccountRepository
from src.domain.value_objects.money import Money
from src.infrastructure.database.mappers.account_mapper import orm_to_domain
from src.infrastructure.database.models.account_model import AccountORM


class AccountRepositoryImpl(AccountRepository):
    """Acceso a datos real: traduce entre ORM y entidades de dominio."""

    def get_by_id(
        self,
        session: Session,
        account_id: int,
        *,
        for_update: bool = False,
    ) -> Account | None:
        stmt = select(AccountORM).where(AccountORM.id == account_id)
        if for_update:
            # En MySQL/InnoDB genera SELECT ... FOR UPDATE: bloquea la fila hasta fin de transacción.
            stmt = stmt.with_for_update()
        row = session.execute(stmt).scalars().first()
        if row is None:
            return None
        return orm_to_domain(row)

    def get_pair_for_transfer_locked(
        self,
        session: Session,
        from_account_id: int,
        to_account_id: int,
    ) -> tuple[Account, Account]:
        """
        Bloquea siempre primero el id menor, luego el mayor.

        Ejemplo de deadlock evitado:
        - Tx1: transfiere 1→2; sin orden podría bloquear 1 luego 2.
        - Tx2: transfiere 2→1; sin orden podría bloquear 2 luego 1.
        Con orden fijo (min, max), ambas piden el mismo orden de locks.
        """
        low_id, high_id = sorted((from_account_id, to_account_id))

        acc_low = self.get_by_id(session, low_id, for_update=True)
        acc_high = self.get_by_id(session, high_id, for_update=True)

        if acc_low is None or acc_high is None:
            raise AccountNotFoundError("Cuenta no encontrada")

        # Reasignar a "origen" y "destino" reales de la transferencia (no necesariamente low/high).
        from_acc = acc_low if from_account_id == low_id else acc_high
        to_acc = acc_high if to_account_id == high_id else acc_low
        return from_acc, to_acc

    def create(self, session: Session, owner: str, initial_balance: Money) -> Account:
        row = AccountORM(owner=owner, balance=initial_balance.amount)
        session.add(row)
        session.flush()
        return orm_to_domain(row)

    def save(self, session: Session, account: Account) -> None:
        if account.id is None:
            raise ValueError("No se puede guardar una cuenta sin id")
        row = session.get(AccountORM, account.id)
        if row is None:
            raise AccountNotFoundError("Cuenta no encontrada")
        row.owner = account.owner
        row.balance = account.balance.amount
