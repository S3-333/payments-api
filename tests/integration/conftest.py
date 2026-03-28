import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.base import Base

TEST_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/payments_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)