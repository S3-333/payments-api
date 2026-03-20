from sqlalchemy.orm import Session
from src.infrastructure.database.models.account_model import Account


def create_account(db: Session, owner: str, initial_balance: float = 0):
    account = Account(
        owner=owner,
        balance=initial_balance
    )

    db.add(account)      # Se agrega a la sesión (no a la DB todavía)
    db.commit()          # Se guarda en la base de datos
    db.refresh(account)  # Se actualiza el objeto (ej: id generado)

    return account