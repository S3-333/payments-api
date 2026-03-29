# =============================================================================
# Caso de uso: transferir dinero entre dos cuentas.
#
# Orquesta: validación de reglas -> bloqueo de filas (repositorio) -> actualizar saldos
# -> escribir fila en libro de transferencias -> UN SOLO commit.
#
# Si lees un solo archivo de "lógica", que sea este o el repositorio (account_repository_impl).
# =============================================================================

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from src.domain.exceptions import (
    DomainError,
    InsufficientFundsError,
    InvalidTransferError,
)
from src.domain.repositories.account_repository import AccountRepository
from src.domain.repositories.transfer_ledger_repository import TransferLedgerRepository
from src.domain.value_objects.money import Money


class TransferMoneyUseCase:
    """
    Flujo:
    1) Validar monto > 0 mediante Money.as_transfer_amount.
    2) Bloquear cuentas en orden de id (implementado en el repositorio).
    3) Comprobar saldo suficiente.
    4) Debitar / acreditar usando value objects inmutables.
    5) Registrar fila en tabla de transacciones (auditoría).
    6) Un solo commit.

    Si algo falla, rollback único.
    """

    def __init__(
        self,
        accounts: AccountRepository,
        ledger: TransferLedgerRepository,
    ) -> None:
        self._accounts = accounts
        self._ledger = ledger

    def execute(
        self,
        session: Session,
        from_account_id: int,
        to_account_id: int,
        amount: Decimal,
    ) -> None:
        # --- Reglas rápidas en memoria (antes de tocar la BD) ---
        if from_account_id == to_account_id:
            raise InvalidTransferError("No se puede transferir a la misma cuenta")

        # Money valida que el monto sea > 0; si no, ValueError -> la convertimos a DomainError
        try:
            transfer_amount = Money.as_transfer_amount(amount)
        except ValueError as e:
            raise InvalidTransferError(str(e)) from e

        try:
            # --- Dentro de una transacción SQL (hasta commit/rollback) ---
            # El repositorio hace SELECT ... FOR UPDATE en orden de id (ver implementación).
            from_acc, to_acc = self._accounts.get_pair_for_transfer_locked(
                session,
                from_account_id,
                to_account_id,
            )

            if from_acc.balance < transfer_amount:
                raise InsufficientFundsError("Saldo insuficiente")

            # subtract/add devuelven nuevos Money (inmutables); actualizamos la entidad mutable
            new_from = from_acc.balance.subtract(transfer_amount)
            new_to = to_acc.balance.add(transfer_amount)
            from_acc.balance = new_from
            to_acc.balance = new_to

            # Persistimos cambios en las filas ORM asociadas
            self._accounts.save(session, from_acc)
            self._accounts.save(session, to_acc)

            # Misma transacción: insert en tabla de historial de transferencias
            self._ledger.append_transfer(
                session,
                from_account_id,
                to_account_id,
                transfer_amount,
            )

            session.commit()
        except DomainError:
            # Cualquier DomainError (saldo, cuenta no encontrada desde repo, etc.): rollback y re-lanzar
            session.rollback()
            raise
        except Exception:
            # Errores técnicos (conexión, SQL raro): rollback y propagar (suelen ser 500)
            session.rollback()
            raise
