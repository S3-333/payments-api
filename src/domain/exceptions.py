# Errores de dominio: separan fallos de reglas de negocio de errores técnicos (HTTP 500).
# Así la capa de presentación puede mapear DomainError -> 400 y Exception -> 500.


class DomainError(Exception):
    """Base para cualquier violación de reglas de negocio acordadas en el dominio."""

    pass


class InsufficientFundsError(DomainError):
    """Se intentó debitar más dinero del disponible en la cuenta."""

    pass


class AccountNotFoundError(DomainError):
    """No existe una cuenta con el identificador indicado."""

    pass


class InvalidTransferError(DomainError):
    """Transferencia inválida: mismo origen y destino, monto no positivo, etc."""

    pass


class InvalidInitialBalanceError(DomainError):
    """El saldo inicial no puede ser negativo (regla de negocio del producto)."""

    pass
