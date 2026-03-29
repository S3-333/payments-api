# Pruebas unitarias del caso de uso de transferencia con repositorios en memoria (sin MySQL).

from decimal import Decimal

import pytest

from src.application.use_cases.transfer_money import TransferMoneyUseCase
from src.domain.entities.account import Account
from src.domain.exceptions import AccountNotFoundError, InsufficientFundsError, InvalidTransferError
from src.domain.value_objects.money import Money
from tests.fakes import FakeAccountRepository, FakeLedger, FakeSession, FailingSaveRepository


def test_transfer_success() -> None:
    repo = FakeAccountRepository()
    acc1 = Account(id=1, owner="Juan", balance=Money.from_decimal("100.00"))
    acc2 = Account(id=2, owner="Ana", balance=Money.from_decimal("50.00"))
    repo.add_account(acc1)
    repo.add_account(acc2)

    db = FakeSession()
    uc = TransferMoneyUseCase(repo, FakeLedger())
    uc.execute(db, 1, 2, Decimal("30.00"))

    assert acc1.balance.amount == Decimal("70.00")
    assert acc2.balance.amount == Decimal("80.00")


def test_transfer_insufficient_balance() -> None:
    repo = FakeAccountRepository()
    acc1 = Account(id=1, owner="Juan", balance=Money.from_decimal("10.00"))
    acc2 = Account(id=2, owner="Ana", balance=Money.from_decimal("50.00"))
    repo.add_account(acc1)
    repo.add_account(acc2)

    db = FakeSession()
    uc = TransferMoneyUseCase(repo, FakeLedger())

    with pytest.raises(InsufficientFundsError):
        uc.execute(db, 1, 2, Decimal("30.00"))


def test_account_not_found() -> None:
    repo = FakeAccountRepository()
    acc1 = Account(id=1, owner="Juan", balance=Money.from_decimal("100.00"))
    repo.add_account(acc1)

    db = FakeSession()
    uc = TransferMoneyUseCase(repo, FakeLedger())

    with pytest.raises(AccountNotFoundError):
        uc.execute(db, 1, 2, Decimal("10.00"))


def test_invalid_amount() -> None:
    repo = FakeAccountRepository()
    acc1 = Account(id=1, owner="Juan", balance=Money.from_decimal("100.00"))
    acc2 = Account(id=2, owner="Ana", balance=Money.from_decimal("50.00"))
    repo.add_account(acc1)
    repo.add_account(acc2)

    db = FakeSession()
    uc = TransferMoneyUseCase(repo, FakeLedger())

    with pytest.raises(InvalidTransferError):
        uc.execute(db, 1, 2, Decimal("0"))


def test_same_account_transfer() -> None:
    repo = FakeAccountRepository()
    acc1 = Account(id=1, owner="Juan", balance=Money.from_decimal("100.00"))
    repo.add_account(acc1)
    db = FakeSession()
    uc = TransferMoneyUseCase(repo, FakeLedger())
    with pytest.raises(InvalidTransferError):
        uc.execute(db, 1, 1, Decimal("10.00"))


def test_rollback_on_error() -> None:
    repo = FailingSaveRepository()
    acc1 = Account(id=1, owner="Juan", balance=Money.from_decimal("100.00"))
    acc2 = Account(id=2, owner="Ana", balance=Money.from_decimal("50.00"))
    repo.add_account(acc1)
    repo.add_account(acc2)

    db = FakeSession()
    uc = TransferMoneyUseCase(repo, FakeLedger())

    with pytest.raises(RuntimeError):
        uc.execute(db, 1, 2, Decimal("10.00"))

    assert db.rolled_back is True
    assert db.committed is False
