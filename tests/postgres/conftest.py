import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from postgres import get_pg_engine


@pytest.fixture(scope="session")
def pg_engine():
    e = get_pg_engine()
    yield e
    e.dispose()


@pytest.fixture(autouse=True)
def truncate_table(pg_engine):
    with Session(pg_engine) as session:
        session.execute(text('TRUNCATE TABLE dbo."AppUser" RESTART IDENTITY'))
        session.commit()
