# Conversión entre capas: el dominio no debe importar SQLAlchemy.

from __future__ import annotations

from src.domain.entities.account import Account
from src.domain.value_objects.money import Money
from src.infrastructure.database.models.account_model import AccountORM


def orm_to_domain(row: AccountORM) -> Account:
    """Convierte fila ORM a entidad de dominio con Money."""
    return Account(
        id=row.id,
        owner=row.owner,
        balance=Money.from_decimal(row.balance),
    )
