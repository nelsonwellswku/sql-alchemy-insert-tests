import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

PG_SERVER = os.getenv("PG_SERVER", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_NAME = os.getenv("PG_NAME", "postgres")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")


def _pg_url() -> str:
    password = quote_plus(PG_PASSWORD)
    return f"postgresql+psycopg2://{PG_USER}:{password}@{PG_SERVER}:{PG_PORT}/{PG_NAME}"


def get_pg_engine():
    return create_engine(_pg_url())
