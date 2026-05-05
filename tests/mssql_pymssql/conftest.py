import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from mssql_pymssql import get_engine


@pytest.fixture(scope="session")
def engine():
    e = get_engine()
    yield e
    e.dispose()


@pytest.fixture(autouse=True)
def truncate_table(engine):
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE dbo.AppUser"))
        session.commit()
