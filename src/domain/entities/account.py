# Entidad de dominio Account: describe qué es una cuenta en el negocio,
# sin detalles de SQL ni SQLAlchemy. La persistencia la adapta la infraestructura.

from __future__ import annotations

from dataclasses import dataclass

from src.domain.value_objects.money import Money


@dataclass
class Account:
    """
    Cuenta bancaria lógica: titular + saldo.

    id puede ser None antes de persistir (creación en memoria).
    """

    id: int | None
    owner: str
    balance: Money
