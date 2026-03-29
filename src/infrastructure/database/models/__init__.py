# Importar todos los modelos aquí permite que Alembic vea el metadata completo
# (autogenerate) y que Base.metadata.create_all tenga todas las tablas.

from src.infrastructure.database.models.account_model import AccountORM
from src.infrastructure.database.models.transaction_model import TransferRecordORM

__all__ = ["AccountORM", "TransferRecordORM"]
