import time

from sqlalchemy import insert, text
from sqlalchemy.orm import Session

from models import AppUser


def test_standard_add_all(engine, user_rows):
    """Insert 50k rows using Session.add_all() + Session.commit()."""
    objects = [AppUser(**row) for row in user_rows]

    start = time.perf_counter()
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pymssql standard add_all] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert(engine, user_rows):
    """Insert 50k rows using SQLAlchemy 2.0 ORM bulk insert."""
    start = time.perf_counter()
    with Session(engine) as session:
        session.execute(insert(AppUser).execution_options(render_nulls=True), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pymssql orm bulk insert] elapsed: {elapsed:.3f}s")


def test_raw_sql_bulk_insert(engine, user_rows):
    """Insert 50k rows using session.execute(text(...)) with raw SQL."""
    sql = text(
        "INSERT INTO dbo.AppUser (FirstName, LastName, Birthday, Gender, Ethnicity)"
        " VALUES (:FirstName, :LastName, :Birthday, :Gender, :Ethnicity)"
    )

    start = time.perf_counter()
    with Session(engine) as session:
        session.execute(sql, user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pymssql raw sql bulk insert] elapsed: {elapsed:.3f}s")
