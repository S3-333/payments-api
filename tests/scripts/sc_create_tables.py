# Script opcional: crea tablas desde los modelos SQLAlchemy (equivalente rough a migrate).
# En producción se prefiere `alembic upgrade head` para historial y revisiones explícitas.

from src.infrastructure.database.base import Base
from src.infrastructure.database.database import engine

# Registrar todos los modelos en Base.metadata (accounts + transfer_records).
from src.infrastructure.database.models import AccountORM, TransferRecordORM  # noqa: F401


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas (si no existian).")


if __name__ == "__main__":
    main()
