import time

from sqlalchemy import insert, text
from sqlalchemy.orm import Session

from models import AppUser


def test_standard_add_all(pg3_engine, user_rows):
    """Insert 50k rows using Session.add_all() + Session.commit()."""
    objects = [AppUser(**row) for row in user_rows]

    start = time.perf_counter()
    with Session(pg3_engine) as session:
        session.add_all(objects)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pg3 standard add_all] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert(pg3_engine, user_rows):
    """Insert 50k rows using SQLAlchemy 2.0 ORM bulk insert."""
    start = time.perf_counter()
    with Session(pg3_engine) as session:
        session.execute(insert(AppUser).execution_options(render_nulls=True), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pg3 orm bulk insert] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert_pipeline(pg3_fast_engine, user_rows):
    """Insert 50k rows using ORM bulk insert with psycopg3 pipeline mode."""
    start = time.perf_counter()
    with Session(pg3_fast_engine) as session:
        session.execute(insert(AppUser), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pg3 orm bulk insert + pipeline] elapsed: {elapsed:.3f}s")


def test_raw_sql_bulk_insert(pg3_engine, user_rows):
    """Insert 50k rows using session.execute(text(...)) with raw SQL."""
    sql = text(
        'INSERT INTO dbo."AppUser" ("FirstName", "LastName", "Birthday", "Gender", "Ethnicity")'
        " VALUES (:FirstName, :LastName, :Birthday, :Gender, :Ethnicity)"
    )

    start = time.perf_counter()
    with Session(pg3_engine) as session:
        session.execute(sql, user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[pg3 raw sql bulk insert] elapsed: {elapsed:.3f}s")
