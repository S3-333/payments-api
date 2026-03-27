# Se encarga de definir la interfaz del repositorio de cuentas,
# que es una abstracción que define los métodos necesarios 
# para interactuar con las cuentas en la base de datos.
# Esta interfaz es implementada por AccountRepositoryImpl, que contiene la 
# lógica específica de acceso a datos utilizando SQLAlchemy. Al definir esta interfaz, 
# se permite que la lógica de negocio (en AccountService) dependa de una abstracción, 
# lo que facilita el mantenimiento y la posibilidad de cambiar la implementación del 
# repositorio sin afectar la lógica de negocio.

from abc import ABC, abstractmethod


class AccountRepository(ABC):

    @abstractmethod
    def get_by_id(self, db, account_id: int, for_update: bool = False):
        pass

    @abstractmethod
    def save(self, db, account):
        pass