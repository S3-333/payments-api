# Test que simula el comportamiento del sistema de transferencias sin la necesidad de una base de datos real. 
# Se crean cuentas falsas y se prueba la lógica de transferencia, incluyendo casos de éxito, saldo insuficiente, 
# cuenta no encontrada y monto inválido.

from decimal import Decimal
import pytest
from src.domain.services.account_service import transfer_money
from src.domain.repositories.account_repository import AccountRepository

# Class = simulan las entidades y repositorios necesarios para las pruebas.

# Cuenta falsa para pruebas
class FakeAccount:
    def __init__(self, id, owner, balance):
        self.id = id
        self.owner = owner
        self.balance = Decimal(balance)


# Repositorio falso para pruebas
class FakeAccountRepository(AccountRepository):

    def __init__(self):
        self.accounts = {} # Diccionario para almacenar cuentas por ID 

    def add_account(self, account):
        self.accounts[account.id] = account

    def get_by_id(self, db, account_id: int, for_update: bool = False):
        return self.accounts.get(account_id)

    def save(self, db, account):
        self.accounts[account.id] = account


# Repositorio que simula un error al guardar, para probar el manejo de excepciones en la lógica de transferencia.
class FailingRepository(FakeAccountRepository):

    def save(self, db, account):
        raise Exception("Error al guardar")


# Sesión falsa, simula las operaciones de commit y rollback sin hacer nada real. 
class FakeSession:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True



# Tests 

# Prueba de transferencia exitosa entre dos cuentas. Se verifica que los saldos se actualicen correctamente.
def test_transfer_success():
    repo = FakeAccountRepository()
    acc1 = FakeAccount(1, "Juan", "100.00")
    acc2 = FakeAccount(2, "Ana", "50.00")

    repo.add_account(acc1)
    repo.add_account(acc2)

    db = FakeSession()
    transfer_money(db, repo, 1, 2, Decimal("30.00"))

    assert acc1.balance == Decimal("70.00")
    assert acc2.balance == Decimal("80.00")



# Prueba de transferencia con saldo insuficiente. Se espera que se lance una excepción y que los saldos no cambien.
def test_transfer_insufficient_balance():
    repo = FakeAccountRepository()
    db = FakeSession()

    acc1 = FakeAccount(1, "Juan", "10.00")
    acc2 = FakeAccount(2, "Ana", "50.00")

    repo.add_account(acc1)
    repo.add_account(acc2)

    with pytest.raises(ValueError, match="Saldo insuficiente"):
        db = FakeSession()
        transfer_money(db, repo, 1, 2, Decimal("30.00"))


# Prueba de transferencia a una cuenta que no existe.
def test_account_not_found():
    repo = FakeAccountRepository()
   
    acc1 = FakeAccount(1, "Juan", "100.00")
    repo.add_account(acc1)

    with pytest.raises(ValueError, match="Cuenta no encontrada"):
        db = FakeSession()
        transfer_money(db, repo, 1, 2, Decimal("10.00"))


# Prueba de transferencia con monto inválido (0 o negativo).
def test_invalid_amount():
    repo = FakeAccountRepository()
    
    acc1 = FakeAccount(1, "Juan", "100.00")
    acc2 = FakeAccount(2, "Ana", "50.00")

    repo.add_account(acc1)
    repo.add_account(acc2)

    with pytest.raises(ValueError, match="mayor a 0"):
        transfer_money(None, repo, 1, 2, Decimal("0"))


# Prueba que simula un error al guardar las cuentas después de la transferencia, 
# para verificar que se realice un rollback de la transacción.
def test_rollback_on_error():
    repo = FailingRepository()
    db = FakeSession()

    acc1 = FakeAccount(1, "Juan", "100.00")
    acc2 = FakeAccount(2, "Ana", "50.00")

    repo.add_account(acc1)
    repo.add_account(acc2)

    with pytest.raises(Exception):
        transfer_money(db, repo, 1, 2, Decimal("10.00"))

    assert db.rolled_back is True
    assert db.committed is False