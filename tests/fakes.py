# Fakes compartidos para pruebas: repositorios en memoria y sesión simulada.
# Evitamos duplicar estas clases en cada archivo de test.

from src.domain.entities.account import Account
from src.domain.exceptions import AccountNotFoundError
from src.domain.repositories.account_repository import AccountRepository
from src.domain.repositories.transfer_ledger_repository import TransferLedgerRepository
from src.domain.value_objects.money import Money


class FakeSession:
    """Sesión mínima: solo rastrea commit/rollback para aserciones."""

    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True


class FakeLedger(TransferLedgerRepository):
    """Ledger en memoria: no persiste filas; cumple el contrato del caso de uso."""

    def append_transfer(self, session, from_account_id, to_account_id, amount: Money) -> None:
        return None


class FakeAccountRepository(AccountRepository):
    """Repositorio en memoria para pruebas unitarias del dominio."""

    def __init__(self) -> None:
        self.accounts: dict[int, Account] = {}

    def add_account(self, account: Account) -> None:
        self.accounts[account.id] = account

    def get_by_id(self, session, account_id: int, *, for_update: bool = False) -> Account | None:
        return self.accounts.get(account_id)

    def get_pair_for_transfer_locked(
        self,
        session,
        from_account_id: int,
        to_account_id: int,
    ) -> tuple[Account, Account]:
        low_id, high_id = sorted((from_account_id, to_account_id))
        acc_low = self.accounts.get(low_id)
        acc_high = self.accounts.get(high_id)
        if acc_low is None or acc_high is None:
            raise AccountNotFoundError("Cuenta no encontrada")
        from_acc = acc_low if from_account_id == low_id else acc_high
        to_acc = acc_high if to_account_id == high_id else acc_low
        return from_acc, to_acc

    def create(self, session, owner: str, initial_balance: Money) -> Account:
        new_id = max(self.accounts.keys(), default=0) + 1
        acc = Account(id=new_id, owner=owner, balance=initial_balance)
        self.accounts[new_id] = acc
        return acc

    def save(self, session, account: Account) -> None:
        self.accounts[account.id] = account


class FailingSaveRepository(FakeAccountRepository):
    """Simula fallo al guardar (error de infraestructura)."""

    def save(self, session, account: Account) -> None:
        raise RuntimeError("Error al guardar")
