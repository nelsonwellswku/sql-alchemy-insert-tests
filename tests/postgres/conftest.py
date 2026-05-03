import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from main import get_pg_engine, get_pg_fast_engine

NUM_ROWS = 50_000


@pytest.fixture(scope="session")
def pg_engine():
    e = get_pg_engine()
    yield e
    e.dispose()


@pytest.fixture(scope="session")
def pg_fast_engine():
    e = get_pg_fast_engine()
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
def truncate_table(pg_engine):
    with Session(pg_engine) as session:
        session.execute(text('TRUNCATE TABLE dbo."AppUser" RESTART IDENTITY'))
        session.commit()
