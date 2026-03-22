#Codigo de prueba, para probar la funcion de crear cuenta, se puede ejecutar este archivo 
# directamente para probarlo

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.crud.account_crud import create_account


def main():
    db = SessionLocal()

    try:
        acc1 = create_account(db, "Santiago", 1000)
        acc2 = create_account(db, "Juan", 500)
        acc3 = create_account(db, "Maria", 200)

        print("Cuentas creadas:")
        print(acc1.id, acc1.owner, acc1.balance)
        print(acc2.id, acc2.owner, acc2.balance)
        print(acc3.id, acc3.owner, acc3.balance)

    finally:
        db.close()


if __name__ == "__main__":
    main()