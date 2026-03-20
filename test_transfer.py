from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.crud.account_crud import transfer_money


def main():
    db = SessionLocal()

    try:
        from_acc, to_acc = transfer_money(db, 2, 99, 30)

        print("Transferencia exitosa")
        print("Cuenta origen:", from_acc.balance)
        print("Cuenta destino:", to_acc.balance)

    except Exception as e:
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()