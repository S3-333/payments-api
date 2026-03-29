# Base declarativa de SQLAlchemy: todas las tablas ORM heredan de Base para compartir metadata.
# Alembic y create_all() usan Base.metadata para conocer el esquema completo.

from sqlalchemy.orm import declarative_base

Base = declarative_base()