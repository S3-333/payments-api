# Puerto (interfaz) del repositorio de cuentas: el dominio define QUÉ necesita,
# la infraestructura define CÓMO (SQLAlchemy, MySQL, etc.).
# Esto permite tests con implementaciones en memoria sin base de datos real.

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from src.domain.entities.account import Account
from src.domain.value_objects.money import Money


class AccountRepository(ABC):
    """Contrato para leer y escribir cuentas."""

    @abstractmethod
    def get_by_id(
        self,
        session: Session,
        account_id: int,
        *,
        for_update: bool = False,
    ) -> Account | None:
        """Obtiene una cuenta por id; for_update=True aplica bloqueo de fila (SELECT ... FOR UPDATE)."""
        pass

    @abstractmethod
    def get_pair_for_transfer_locked(
        self,
        session: Session,
        from_account_id: int,
        to_account_id: int,
    ) -> tuple[Account, Account]:
        """
        Obtiene origen y destino bloqueando filas SIEMPRE en orden creciente de id.

        Así dos transferencias concurrentes A→B y B→A piden los locks en el mismo orden
        y se evitan deadlocks circulares entre transacciones.
        """
        pass

    @abstractmethod
    def create(self, session: Session, owner: str, initial_balance: Money) -> Account:
        """Inserta una cuenta nueva; no hace commit (lo decide el caso de uso)."""
        pass

    @abstractmethod
    def save(self, session: Session, account: Account) -> None:
        """Persiste cambios de una cuenta ya existente (balance actualizado, etc.)."""
        pass
