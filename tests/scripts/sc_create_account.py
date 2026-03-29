# Script manual: crea cuentas de ejemplo usando el caso de uso (misma ruta que la API).

from decimal import Decimal

from src.application.use_cases.create_account import CreateAccountUseCase
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.repositories.account_repository_impl import AccountRepositoryImpl


def main() -> None:
    db = SessionLocal()
    try:
        uc = CreateAccountUseCase(AccountRepositoryImpl())
        acc1 = uc.execute(db, "Santiago", Decimal("1000.00"))
        acc2 = uc.execute(db, "Juan", Decimal("500.00"))
        acc3 = uc.execute(db, "Maria", Decimal("200.00"))

        print("Cuentas creadas:")
        print(acc1.id, acc1.owner, acc1.balance.amount)
        print(acc2.id, acc2.owner, acc2.balance.amount)
        print(acc3.id, acc3.owner, acc3.balance.amount)
    finally:
        db.close()


if __name__ == "__main__":
    main()
