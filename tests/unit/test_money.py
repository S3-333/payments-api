# Pruebas del value object Money: reglas de construcción y operaciones seguras.

from decimal import Decimal

import pytest

from src.domain.value_objects.money import Money


def test_money_from_decimal_rounds() -> None:
    # HALF_EVEN (por defecto en quantize): 10.125 -> 10.12 (par más cercano en el último dígito).
    m = Money.from_decimal(Decimal("10.125"))
    assert m.amount == Decimal("10.12")


def test_transfer_amount_rejects_zero() -> None:
    with pytest.raises(ValueError):
        Money.as_transfer_amount(Decimal("0"))


def test_subtract() -> None:
    a = Money.from_decimal("100.00")
    b = Money.from_decimal("30.50")
    assert a.subtract(b).amount == Decimal("69.50")


def test_negative_money_rejected() -> None:
    with pytest.raises(ValueError):
        Money.from_decimal(Decimal("-1"))
