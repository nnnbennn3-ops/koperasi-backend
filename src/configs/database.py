from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.configs.config import settings

odbc_str = (
    f"DRIVER={{{settings.db_driver}}};"
    f"SERVER={settings.db_server},{settings.db_port};"
    f"DATABASE={settings.db_name};"
    f"UID={settings.db_user};"
    f"PWD={settings.db_password};"
    "TrustServiceCertificate=yes;"
)

connection_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_str)}"

engine = create_engine(
    connection_url, pool_pre_ping=True, pool_size=10, max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
