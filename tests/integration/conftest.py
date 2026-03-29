# Fixtures de integración: motor SQLite en memoria para no exigir MySQL en CI o máquinas sin Docker.
# Las pruebas siguen usando los mismos repositorios SQLAlchemy que en producción (misma lógica SQL).

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.base import Base

# Importar modelos para registrar tablas en Base.metadata.
from src.infrastructure.database.models import AccountORM, TransferRecordORM  # noqa: F401


@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    Una base nueva por test: aislamiento total entre casos.

    SQLite no replica todos los matices de bloqueo de MySQL; las pruebas de FOR UPDATE
    exhaustivas conviene ejecutarlas contra MySQL en un entorno dedicado.
    """
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
