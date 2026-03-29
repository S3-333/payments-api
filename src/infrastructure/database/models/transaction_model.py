# Tabla de movimientos: cada transferencia genera una fila (auditoría, trazabilidad).

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class TransferRecordORM(Base):
    """
    Registro de una transferencia completada.

    No sustituye el libro contable completo de un banco real, pero permite:
    - listar historial por cuenta
    - reconciliar saldos
    - investigar disputas
    """

    __tablename__ = "transfer_records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)

    amount = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
