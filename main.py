import datetime

from sqlalchemy.orm import Session

from models import AppUser
from mssql import DB_SERVER, DB_PORT, DB_NAME, get_engine


def main():
    print(f"Connecting to {DB_SERVER}:{DB_PORT}/{DB_NAME} ...")
    engine = get_engine()

    user = AppUser(
        FirstName="Jane",
        LastName="Doe",
        Birthday=datetime.date(1990, 6, 15),
        Gender="F",
        Ethnicity="Hispanic",
    )

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        fetched = session.get(AppUser, user.AppUserId)

    if fetched is None:
        print("Error: inserted user could not be retrieved.")
        return

    print("Inserted and retrieved AppUser:")
    print(f"  AppUserId : {fetched.AppUserId}")
    print(f"  FirstName : {fetched.FirstName}")
    print(f"  LastName  : {fetched.LastName}")
    print(f"  Birthday  : {fetched.Birthday}")
    print(f"  Gender    : {fetched.Gender}")
    print(f"  Ethnicity : {fetched.Ethnicity}")


if __name__ == "__main__":
    main()
