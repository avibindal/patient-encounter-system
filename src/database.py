import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Prefer DATABASE_URL when provided; otherwise default to a local SQLite file.
# This makes local development and CI simpler and avoids MySQL-specific behavior.
database_url = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

engine = create_engine(database_url, echo=False)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)
