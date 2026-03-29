# Modelo ORM SQLAlchemy: representa la tabla `accounts` en MySQL.
# Es independiente de la entidad de dominio `Account` (src/domain/entities/); el mapper convierte entre ambos.

from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class AccountORM(Base):
    """
    Tabla de cuentas: id, titular, saldo (Numeric), fecha de creación.

    Numeric(12,2) evita float; MySQL almacena DECIMAL exacto.
    """

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner = Column(String(100), nullable=False)

    # DECIMAL(12,2): hasta 9999999999.99 — suficiente para este ejercicio.
    balance = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
