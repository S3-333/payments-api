# Prueba del caso de uso de creación de cuenta (repositorio falso + sesión falsa).

from decimal import Decimal

import pytest

from src.application.use_cases.create_account import CreateAccountUseCase
from src.domain.exceptions import InvalidInitialBalanceError
from src.domain.value_objects.money import Money
from tests.fakes import FakeAccountRepository, FakeSession


def test_create_account_success() -> None:
    repo = FakeAccountRepository()
    db = FakeSession()
    uc = CreateAccountUseCase(repo)
    acc = uc.execute(db, "Ana", Decimal("50.00"))
    assert acc.owner == "Ana"
    assert acc.balance == Money.from_decimal("50.00")
    assert acc.id is not None
    assert db.committed is True


def test_create_account_negative_balance() -> None:
    repo = FakeAccountRepository()
    db = FakeSession()
    uc = CreateAccountUseCase(repo)
    with pytest.raises(InvalidInitialBalanceError):
        uc.execute(db, "Ana", Decimal("-1.00"))
