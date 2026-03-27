# Codigo de prueba para crear las tablas en la base de datos, se ejecuta una sola vez para crear las tablas a partir de los modelos definidos
# En este caso, se crea la tabla accounts a partir del modelo Account definido en account_model.py 

from src.infrastructure.database.database import engine
from src.infrastructure.database.models.account_model import Base

Base.metadata.create_all(bind=engine)