import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from psycopg3 import get_pg3_engine


@pytest.fixture(scope="session")
def pg3_engine():
    e = get_pg3_engine()
    yield e
    e.dispose()


@pytest.fixture(autouse=True)
def truncate_table(pg3_engine):
    with Session(pg3_engine) as session:
        session.execute(text('TRUNCATE TABLE dbo."AppUser" RESTART IDENTITY'))
        session.commit()
