
# Una session es una conexion activa, como una operacion en curso
from sqlalchemy.orm import Session # Importamos Session para manejar la sesión de la base de datos
from src.infrastructure.database.models.account_model import Account # Importamos el modelo de account


# Crea una cuenta
def create_account(db: Session, owner: str, initial_balance: float = 0): #db es una instancia de session, se pasa desde afuera normalmente desde la api
    account = Account(
        owner=owner,
        balance=initial_balance
    ) # Solo campos lo caules no son autogenerados (id, created_at se son autogenerados)

    db.add(account)      # Se agregan a la sesión (no a la DB todavía)
    db.commit()          # Se guarda en la base de datos
    db.refresh(account)  # Se actualiza el objeto (ej: id generado)

    return account



# Funcion para obtener una cuenta por su ID, devuelve el primer resultado o None si no se encuentra
def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first() # Consulta la cuenta por id, devuelve el primer resultado o None
    # Query sirve para entrar en la tabla, filter para aplicar un filtro (en este caso donde el id de la tabla 
    # sea igual al id del parametro) y first para obtener el primer resultado



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