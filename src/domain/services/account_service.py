from decimal import Decimal
from sqlalchemy.orm import Session
from src.domain.repositories.account_repository import AccountRepository


def transfer_money(
    db: Session,
    repo: AccountRepository, # Repo contiene la lógica de acceso a datos, es decir, cómo se obtienen y guardan las cuentas en la base de datos.
    from_account_id: int,
    to_account_id: int,
    amount: Decimal
):
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0")

    try:
        # Busca las cuentas de origen y destino de la transferencia (Pero con bloqeo para evitar race conditions)
        from_account = repo.get_by_id(db, from_account_id, for_update=True)
        to_account = repo.get_by_id(db, to_account_id, for_update=True)

        # Si alguna de las cuentas no existe, error
        if not from_account or not to_account:
            raise ValueError("Cuenta no encontrada")

        #Si la cuenta de origen no tiene suficiente saldo, error
        if from_account.balance < amount:
            raise ValueError("Saldo insuficiente")

        
        from_account.balance -= amount # Resta el monto de la cuenta de origen
        to_account.balance += amount # Suma el monto a la cuenta de destino

        # Persistencia delegada
        repo.save(db, from_account)
        repo.save(db, to_account)

        db.commit() # 

        return from_account, to_account
    
    # Si ocurre cualquier error durante la transferencia, se hace rollback, es decir, se deshacen 
    # los cambios realizados en la sesión, para evitar problematicas.
    except Exception as e:
        db.rollback()
        raise e