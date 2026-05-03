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

PG_SERVER = os.getenv("PG_SERVER", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_NAME = os.getenv("PG_NAME", "postgres")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")


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


def _pg_url() -> str:
    password = quote_plus(PG_PASSWORD)
    return f"postgresql+psycopg2://{PG_USER}:{password}@{PG_SERVER}:{PG_PORT}/{PG_NAME}"


def _pg3_url() -> str:
    password = quote_plus(PG_PASSWORD)
    return f"postgresql+psycopg://{PG_USER}:{password}@{PG_SERVER}:{PG_PORT}/{PG_NAME}"


def get_engine():
    return create_engine(_odbc_url())


def get_fast_engine():
    return create_engine(_odbc_url(), fast_executemany=True, use_insertmanyvalues=False)


def get_pg_engine():
    return create_engine(_pg_url())


def get_pg_fast_engine():
    return create_engine(_pg_url(), executemany_mode="values_plus_batch")


def get_pg3_engine():
    return create_engine(_pg3_url())


def get_pg3_fast_engine():
    # psycopg3 pipeline mode batches round-trips for bulk insert performance
    return create_engine(_pg3_url()).execution_options(psycopg_pipeline_mode=True)



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
