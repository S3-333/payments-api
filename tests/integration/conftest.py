import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.base import Base

TEST_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/payments_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

# Sesion de prueba para testear la base de datos, se crea una nueva sesión para cada test y se limpia después de cada test
@pytest.fixture(scope="function") # scope "function" para que se ejecute antes y después de cada test
def db():
    Base.metadata.create_all(bind=engine) # Crea las tablas

    session = TestingSessionLocal() # Crea sesión de prueba

    yield session # Devuelve la sesión para que se use en los tests

    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine) # Borra las tablas 
