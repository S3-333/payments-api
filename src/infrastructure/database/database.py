# =============================================================================
# Conexión a la base de datos (infraestructura).
#
# Este módulo define:
# - engine: "motor" global de SQLAlchemy (pool de conexiones)
# - SessionLocal: fábrica de sesiones (cada sesión = una unidad de trabajo / transacción lógica)
#
# Quién usa SessionLocal: src/presentation/api/deps.py -> get_db() -> yield session a la ruta.
# =============================================================================

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Busca archivo .env en el cwd (al ejecutar desde la raíz del proyecto encuentra ./.env)
load_dotenv()

# Cadena de conexión: debe coincidir con docker-compose (usuario, password, base, puerto)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://user:password@localhost:3306/payments",
)

# echo: si true, imprime cada SQL (útil para aprender; ruidoso en producción)
engine = create_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "false").lower() == "true")

# sessionmaker crea una CLASE de sesión; cada llamada SessionLocal() = nueva sesión
# autocommit=False -> hace falta commit() explícito (lo hacen los casos de uso)
# autoflush=False -> no mandamos SQL intermedio hasta flush/commit salvo que lo pidamos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_connection() -> None:
    """Script manual para verificar conectividad (python -m src.infrastructure.database.database)."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Resultado:", result.scalar())
            print("Conexion OK")
    except Exception as e:
        print("Error de conexion:", e)


if __name__ == "__main__":
    test_connection()
