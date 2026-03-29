# Simulación de concurrencia: varias transferencias concurrentes sobre las mismas cuentas.
# SQLite en archivo compartido permite que varios hilos abran sesiones distintas sobre la misma BD.
# (Con :memory: cada conexión ve una base vacía distinta; por eso no sirve para este test.)

import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.application.use_cases.transfer_money import TransferMoneyUseCase
from src.infrastructure.database.base import Base
from src.infrastructure.database.models import AccountORM, TransferRecordORM  # noqa: F401
from src.infrastructure.database.repositories.account_repository_impl import AccountRepositoryImpl
from src.infrastructure.database.repositories.transfer_ledger_repository_impl import (
    TransferLedgerRepositoryImpl,
)


@pytest.fixture(scope="module")
def concurrent_engine():
    """Archivo temporal: una sola base compartida entre hilos y sesiones."""
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    engine = create_engine(
        f"sqlite+pysqlite:///{path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        os.unlink(path)


def _run_transfer(engine, from_id: int, to_id: int, amount: str) -> None:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session: Session = SessionLocal()
    try:
        uc = TransferMoneyUseCase(AccountRepositoryImpl(), TransferLedgerRepositoryImpl())
        uc.execute(session, from_id, to_id, Decimal(amount))
    finally:
        session.close()


def test_concurrent_transfers_balance_consistent(concurrent_engine) -> None:
    SessionLocal = sessionmaker(bind=concurrent_engine)
    setup = SessionLocal()
    try:
        a = AccountORM(owner="A", balance=Decimal("100000.00"))
        b = AccountORM(owner="B", balance=Decimal("100000.00"))
        setup.add(a)
        setup.add(b)
        setup.commit()
        setup.refresh(a)
        setup.refresh(b)
        id_a, id_b = a.id, b.id
    finally:
        setup.close()

    futures = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for _ in range(20):
            futures.append(pool.submit(_run_transfer, concurrent_engine, id_a, id_b, "5.00"))
            futures.append(pool.submit(_run_transfer, concurrent_engine, id_b, id_a, "5.00"))
        for f in as_completed(futures):
            f.result()

    check = SessionLocal()
    try:
        aa = check.get(AccountORM, id_a)
        bb = check.get(AccountORM, id_b)
        # Conservación: el dinero total no debe crearse ni destruirse (invariante del sistema).
        # Con SQLite concurrente los saldos individuales pueden diferir del caso serial;
        # en MySQL + FOR UPDATE el resultado suele coincidir transferencia a transferencia.
        assert aa.balance + bb.balance == Decimal("200000.00")
        assert aa.balance >= 0 and bb.balance >= 0
    finally:
        check.close()
