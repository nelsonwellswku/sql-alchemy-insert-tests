import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from mssql import get_engine, get_fast_executemany_engine, get_fast_executemany_no_imv_engine


@pytest.fixture(scope="session")
def engine():
    e = get_engine()
    yield e
    e.dispose()


@pytest.fixture(scope="session")
def fast_executemany_engine():
    e = get_fast_executemany_engine()
    yield e
    e.dispose()


@pytest.fixture(scope="session")
def fast_executemany_no_imv_engine():
    e = get_fast_executemany_no_imv_engine()
    yield e
    e.dispose()


@pytest.fixture(autouse=True)
def truncate_table(engine):
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE dbo.AppUser"))
        session.commit()
