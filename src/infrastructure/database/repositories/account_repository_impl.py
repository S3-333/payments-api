# Se encarga de interactuar con la base de datos utilizando SQLAlchemy.
# Implementa los métodos definidos en la interfaz AccountRepository.

from src.domain.repositories.account_repository import AccountRepository
from src.infrastructure.database.models.account_model import Account


class AccountRepositoryImpl(AccountRepository):

    # Obtiene una cuenta por ID.
    # Puede aplicar bloqueo (FOR UPDATE) para evitar concurrencia en transacciones.
    def get_by_id(self, db, account_id: int, for_update: bool = False):
        query = db.query(Account).filter(Account.id == account_id)

        # Si se requiere bloqueo (para transferencias seguras)
        if for_update:
            query = query.with_for_update()

        return query.first()


    # Guarda cambios en una cuenta existente.
    def save(self, db, account):
        db.add(account)


    # Crea una nueva cuenta en la base de datos.
    # No hace commit, eso lo maneja el service.
    def create_account(self, db, owner: str, initial_balance):
        account = Account(
            owner=owner,
            balance=initial_balance
        )

        db.add(account)

        return account