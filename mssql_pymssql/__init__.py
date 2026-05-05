import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "master")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def _pymssql_url() -> str:
    password = quote_plus(DB_PASSWORD)
    return f"mssql+pymssql://{DB_USER}:{password}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


def get_engine():
    return create_engine(_pymssql_url())
