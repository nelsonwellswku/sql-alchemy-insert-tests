import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from mssql_pymssql import get_engine, get_fast_engine

NUM_ROWS = 50_000


@pytest.fixture(scope="session")
def engine():
    e = get_engine()
    yield e
    e.dispose()


@pytest.fixture(scope="session")
def fast_engine():
    e = get_fast_engine()
    yield e
    e.dispose()


@pytest.fixture(scope="session")
def user_rows():
    base_date = datetime.date(1990, 1, 1)
    genders = ["M", "F", "NB", "Other", None]
    ethnicities = ["Hispanic", "White", "Black", "Asian", "Other", None]
    return [
        {
            "FirstName": f"First{i}",
            "LastName": f"Last{i}",
            "Birthday": base_date + datetime.timedelta(days=i % 3650),
            "Gender": genders[i % len(genders)],
            "Ethnicity": ethnicities[i % len(ethnicities)],
        }
        for i in range(NUM_ROWS)
    ]


@pytest.fixture(autouse=True)
def truncate_table(engine):
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE dbo.AppUser"))
        session.commit()
