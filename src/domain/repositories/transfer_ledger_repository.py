# Repositorio del libro de transferencias: registra cada movimiento para auditoría.

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from src.domain.value_objects.money import Money


class TransferLedgerRepository(ABC):
    """Contrato para persistir el historial de transferencias entre cuentas."""

    @abstractmethod
    def append_transfer(
        self,
        session: Session,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
    ) -> None:
        """
        Inserta un registro de transferencia en la tabla de transacciones.
        Debe llamarse dentro de la misma transacción SQL que actualiza los saldos.
        """
        pass
