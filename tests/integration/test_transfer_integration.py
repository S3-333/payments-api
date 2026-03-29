# Test de integración para la función de transferencia de dinero entre cuentas, 
# utilizando una base de datos real (SQLite en memoria) para verificar que la lógica de 
# transferencia funciona correctamente y que los cambios se reflejan en la base de datos.

from decimal import Decimal

from src.domain.services.account_service import transfer_money
from src.infrastructure.database.models.account_model import Account
from src.infrastructure.database.repositories.account_repository_impl import AccountRepositoryImpl


def test_transfer_real_db(db):
    repo = AccountRepositoryImpl()

    acc1 = Account(owner="Juan", balance=Decimal("100.00"))
    acc2 = Account(owner="Ana", balance=Decimal("50.00"))

    db.add(acc1)
    db.add(acc2)
    db.commit()

    transfer_money(db, repo, acc1.id, acc2.id, Decimal("30.00"))

    updated_acc1 = db.get(Account, acc1.id)
    updated_acc2 = db.get(Account, acc2.id)

    assert updated_acc1.balance == Decimal("70.00")
    assert updated_acc2.balance == Decimal("80.00")