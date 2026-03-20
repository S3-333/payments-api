#Codigo de prueba, para probar los crud de account

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.crud.account_crud import create_account


def main():
    db = SessionLocal()

    try:
        account = create_account(db, "Santiago", 1000)
        print(account.id, account.owner, account.balance)
    except Exception as e:
        print("❌ Error:", e)
    finally:
        db.close()


if __name__ == "__main__":
    main()