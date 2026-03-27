# Se realiza la tabla 

from sqlalchemy import Column, Integer, String, Numeric, DateTime
from src.infrastructure.database.base import Base
from sqlalchemy.sql import func


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(100), nullable=False)

    # 👇 IMPORTANTE: usar Numeric bien definido
    balance = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )