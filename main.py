import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "master")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")


def get_engine():
    odbc_params = quote_plus(
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    url = f"mssql+pyodbc:///?odbc_connect={odbc_params}"
    return create_engine(url)


def main():
    print(f"Connecting to {DB_SERVER}:{DB_PORT}/{DB_NAME} ...")
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        row = result.fetchone()
    print("Connected! SQL Server version:")
    if row:
        print(row[0])
    else:
        print("No row returned from SQL query.")


if __name__ == "__main__":
    main()
