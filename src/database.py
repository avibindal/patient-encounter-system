from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

username = "mongouhd_evernorth"
password = "U*dgQkKRuEHe"
host = "cp-15.webhostbox.net"  # e.g., 'localhost', '127.0.0.1', or a remote IP
port = 3306  # Optional, default is 3306
database_name = "mongouhd_evernorth"

database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
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
