import datetime
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import AppUser

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


def get_fast_engine():
    return create_engine(_odbc_url(), connect_args={"fast_executemany": True})


def main():
    print(f"Connecting to {DB_SERVER}:{DB_PORT}/{DB_NAME} ...")
    engine = get_engine()

    user = AppUser(
        FirstName="Jane",
        LastName="Doe",
        Birthday=datetime.date(1990, 6, 15),
        Gender="F",
        Ethnicity="Hispanic",
    )

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        fetched = session.get(AppUser, user.AppUserId)

    if fetched is None:
        print("Error: inserted user could not be retrieved.")
        return

    print("Inserted and retrieved AppUser:")
    print(f"  AppUserId : {fetched.AppUserId}")
    print(f"  FirstName : {fetched.FirstName}")
    print(f"  LastName  : {fetched.LastName}")
    print(f"  Birthday  : {fetched.Birthday}")
    print(f"  Gender    : {fetched.Gender}")
    print(f"  Ethnicity : {fetched.Ethnicity}")


if __name__ == "__main__":
    main()
