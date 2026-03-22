
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
def get_account_by_id(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first() # Consulta la cuenta por id, devuelve el primer resultado o None
    # Query sirve para entrar en la tabla, filter para aplicar un filtro (en este caso donde el id de la tabla 
    # sea igual al id del parametro) y first para obtener el primer resultado
