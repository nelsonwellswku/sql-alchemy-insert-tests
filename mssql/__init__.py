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
ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")


def _odbc_url() -> str:
    odbc_params = quote_plus(
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    return f"mssql+pyodbc:///?odbc_connect={odbc_params}"


def get_engine():
    return create_engine(_odbc_url())


def get_fast_executemany_engine():
    return create_engine(_odbc_url(), fast_executemany=True)


def get_fast_executemany_no_imv_engine():
    return create_engine(_odbc_url(), fast_executemany=True, use_insertmanyvalues=False)
