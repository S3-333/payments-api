from sqlalchemy.orm import Session
from src.infrastructure.database.models.account_model import Account


# Transferencia
def transfer_money(db: Session, from_account_id: int, to_account_id: int, amount: float):
    
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0") # Raise lanza un error, y detiene la ejecucion de la funcion

    try:
        # Busca las cuentas de origen y destino de la transferencia
        # Antes:
            # from_account = db.query(Account).filter(Account.id == from_account_id).first()
            # to_account = db.query(Account).filter(Account.id == to_account_id).first()

        #Ahora con with_for_update() para bloquear las filas de las cuentas durante la transferencia, 
        # evitando problemas de concurrencia (E.g: que se intente transferir desde la misma cuenta al mismo tiempo)
        from_account = (
            db.query(Account)
            .filter(Account.id == from_account_id)
            .with_for_update()
            .first()
        )
        to_account = (
            db.query(Account)
            .filter(Account.id == to_account_id)
            .with_for_update()
            .first()
        )

        # Si alguna de las cuentas no existe, error
        if not from_account or not to_account:
            raise ValueError("Cuenta no encontrada")
        
        #Si la cuenta de origen no tiene suficiente saldo, error
        if from_account.balance < amount:
            raise ValueError("Saldo insuficiente")

        from_account.balance -= amount # Resta el monto de la cuenta de origen
        to_account.balance += amount # Suma el monto a la cuenta de destino

        db.commit()
        db.refresh(from_account)
        db.refresh(to_account)

        return from_account, to_account

    # Si ocurre cualquier error durante la transferencia, se hace rollback, es decir, se deshacen 
    # los cambios realizados en la sesión, para evitar problematicas.
    except Exception as e:
        db.rollback()
        raise e