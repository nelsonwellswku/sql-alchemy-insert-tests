import time

from sqlalchemy import insert
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
        session.execute(insert(AppUser), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[orm bulk insert] elapsed: {elapsed:.3f}s")


def test_orm_bulk_insert_fast_executemany(fast_engine, user_rows):
    """Insert 50k rows using ORM bulk insert with fast_executemany enabled."""
    start = time.perf_counter()
    with Session(fast_engine) as session:
        session.execute(insert(AppUser), user_rows)
        session.commit()
    elapsed = time.perf_counter() - start

    print(f"\n[orm bulk insert + fast_executemany] elapsed: {elapsed:.3f}s")
