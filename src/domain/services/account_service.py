from decimal import Decimal
from sqlalchemy.orm import Session
from src.domain.repositories.account_repository import AccountRepository


# Se encarga de la lógica de negocio para crear una cuenta.
# Valida datos y delega la persistencia al repositorio.
def create_account(
    db: Session,
    repo: AccountRepository,  # Repo maneja acceso a datos
    owner: str,
    initial_balance: Decimal
):
    # Validación: el balance inicial no puede ser negativo
    if initial_balance < 0:
        raise ValueError("El balance inicial no puede ser negativo")

    try:
        # Se crea la cuenta a través del repositorio
        account = repo.create_account(db, owner, initial_balance)

        # Se persiste en la base de datos
        db.commit()

        return account

    # Si ocurre algún error, se hace rollback para evitar inconsistencias
    except Exception as e:
        db.rollback()
        raise e


# Se encarga de la lógica de negocio para transferencias entre cuentas.
def transfer_money(
    db: Session,
    repo: AccountRepository,  # Repo contiene la lógica de acceso a datos
    from_account_id: int,
    to_account_id: int,
    amount: Decimal
):
    # Validación: el monto debe ser mayor a 0
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0")

    try:
        # Busca las cuentas con bloqueo para evitar race conditions
        from_account = repo.get_by_id(db, from_account_id, for_update=True)
        to_account = repo.get_by_id(db, to_account_id, for_update=True)

        # Validación: ambas cuentas deben existir
        if not from_account or not to_account:
            raise ValueError("Cuenta no encontrada")

        # Validación: saldo suficiente
        if from_account.balance < amount:
            raise ValueError("Saldo insuficiente")

        # Lógica de negocio (transferencia)
        from_account.balance -= amount
        to_account.balance += amount

        # Persistencia delegada al repositorio
        repo.save(db, from_account)
        repo.save(db, to_account)

        # Confirmar transacción
        db.commit()

        return from_account, to_account

    # En caso de error, se revierte la transacción
    except Exception as e:
        db.rollback()
        raise e