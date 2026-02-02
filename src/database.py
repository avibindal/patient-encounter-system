import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Construct database URL from environment variables when available.
# This avoids hardcoding credentials in source. Set DATABASE_URL or the
# individual DB_* variables in a local .env (not committed) or in CI.
database_url = os.getenv("DATABASE_URL")

if not database_url:
    db_user = os.getenv("DB_USER", "mongouhd_evernorth")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST", "cp-15.webhostbox.net")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "mongouhd_evernorth")

    if db_pass:
        database_url = (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
    else:
        # Fallback to existing string for backward compatibility when no env provided.
        # Warning: this contains a hardcoded password; prefer setting DB_PASS in env.
        database_url = (
            f"mysql+pymysql://{db_user}:U*dgQkKRuEHe@{db_host}:{db_port}/{db_name}"
        )

engine = create_engine(database_url, echo=True)

# Test the connection (optional)
try:
    with engine.connect() as connection:
        print("Connection to the MySQL database created successfully.")
except Exception as e:
    print(f"Connection failed: {e}")


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)
