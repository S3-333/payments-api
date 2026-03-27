# Se encarga de interactuar con la base de datos utilizando SQLAlchemy. 
# Esta clase implementa los métodos definidos en la interfaz AccountRepository, 
# permitiendo obtener cuentas por ID y guardar cambios en las cuentas.

from src.domain.repositories.account_repository import AccountRepository
from src.infrastructure.database.models.account_model import Account


class AccountRepositoryImpl(AccountRepository):

    def get_by_id(self, db, account_id: int, for_update: bool = False):
        query = db.query(Account).filter(Account.id == account_id)

        if for_update:
            query = query.with_for_update()

        return query.first()

    def save(self, db, account):
        db.add(account)