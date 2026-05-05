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

    print(f"\n[standard add_all] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert(engine, user_rows):
    """Insert 50k rows using SQLAlchemy 2.0 ORM bulk insert."""
    start = time.perf_counter()
    with Session(engine) as session:
        session.execute(insert(AppUser).execution_options(render_nulls=True), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[orm bulk insert] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert_fast_executemany(fast_executemany_engine, user_rows):
    """Insert 50k rows using ORM bulk insert with fast_executemany enabled."""
    start = time.perf_counter()
    with Session(fast_executemany_engine) as session:
        session.execute(insert(AppUser), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[orm bulk insert + fast_executemany] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert_fast_executemany_no_insertmanyvalues(fast_executemany_no_imv_engine, user_rows):
    """Insert 50k rows using ORM bulk insert with fast_executemany=True and use_insertmanyvalues=False."""
    start = time.perf_counter()
    with Session(fast_executemany_no_imv_engine) as session:
        session.execute(insert(AppUser), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[orm bulk insert + fast_executemany, no insertmanyvalues] elapsed: {elapsed:.3f}s")


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

    print(f"\n[raw sql bulk insert] elapsed: {elapsed:.3f}s")


def test_raw_pyodbc_fast_executemany(engine, user_rows):
    """Insert 50k rows using a raw pyodbc cursor with fast_executemany=True.

    Bypasses all SQLAlchemy layers: gets the underlying DBAPI connection directly,
    sets fast_executemany on the cursor, and calls cursor.executemany() with
    pyodbc-style positional '?' placeholders.
    """
    sql = (
        "INSERT INTO dbo.AppUser (FirstName, LastName, Birthday, Gender, Ethnicity)"
        " VALUES (?, ?, ?, ?, ?)"
    )
    rows = [
        (r["FirstName"], r["LastName"], r["Birthday"], r["Gender"], r["Ethnicity"])
        for r in user_rows
    ]

    start = time.perf_counter()
    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.fast_executemany = True
        cursor.executemany(sql, rows)
        conn.commit()
    finally:
        conn.close()
    elapsed = time.perf_counter() - start

    print(f"\n[raw pyodbc fast_executemany] elapsed: {elapsed:.3f}s")
