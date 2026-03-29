# Value Object Money: encapsula cantidades monetarias usando Decimal (nunca float).
# float tiene errores de representación binaria; en finanzas eso es inaceptable.
# frozen=True hace el objeto inmutable: al "cambiar" el monto se crea otra instancia.

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Union


# Precisión estándar para moneda en este proyecto (2 decimales, como centavos).
_QUANT = Decimal("0.01")


def _quantize(value: Decimal) -> Decimal:
    """Redondea a 2 decimales con el modo HALF_EVEN (bancario típico)."""
    return value.quantize(_QUANT)


@dataclass(frozen=True)
class Money:
    """
    Representa una cantidad de dinero no negativa (saldo o monto acumulable).

    Para montos de transferencia usa el factory `Money.as_transfer_amount` que exige > 0.
    """

    amount: Decimal

    def __post_init__(self) -> None:
        # Validación centralizada: ningún Money de saldo debería ser negativo.
        if self.amount < 0:
            raise ValueError("Un saldo monetario no puede ser negativo en este modelo")

    @classmethod
    def zero(cls) -> Money:
        """Saldo inicial por defecto."""
        return cls(_quantize(Decimal("0")))

    @classmethod
    def from_decimal(cls, value: Union[Decimal, str, int, float]) -> Money:
        """
        Construye Money desde Decimal u otros tipos convertibles.
        float solo debería usarse en tests o límites controlados; en API preferimos Decimal.
        """
        if isinstance(value, float):
            value = Decimal(str(value))
        elif not isinstance(value, Decimal):
            value = Decimal(value)
        return cls(_quantize(value))

    @classmethod
    def as_transfer_amount(cls, value: Union[Decimal, str, int]) -> Money:
        """
        Monto que se va a mover entre cuentas: debe ser estrictamente positivo.
        Así la regla "monto válido" vive en un solo sitio.
        """
        m = cls.from_decimal(value)
        if m.amount <= 0:
            raise ValueError("El monto de la transferencia debe ser mayor a 0")
        return m

    def add(self, other: Money) -> Money:
        """Suma inmutable de dos cantidades."""
        return Money.from_decimal(self.amount + other.amount)

    def subtract(self, other: Money) -> Money:
        """
        Resta inmutable. Si el resultado fuera negativo, Money lo rechaza en __post_init__.
        El caso de uso debe validar saldo suficiente antes de llamar a subtract.
        """
        return Money.from_decimal(self.amount - other.amount)

    def __ge__(self, other: Money) -> bool:
        return self.amount >= other.amount

    def __lt__(self, other: Money) -> bool:
        return self.amount < other.amount
