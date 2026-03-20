
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

