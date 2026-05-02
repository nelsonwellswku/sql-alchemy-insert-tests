from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AppUser(Base):
    __tablename__ = "AppUser"
    __table_args__ = {"schema": "dbo"}

    AppUserId: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    FirstName: Mapped[str | None] = mapped_column(String(100), nullable=True)
    LastName: Mapped[str | None] = mapped_column(String(100), nullable=True)
    Birthday: Mapped[Date | None] = mapped_column(Date, nullable=True)
    Gender: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Ethnicity: Mapped[str | None] = mapped_column(String(100), nullable=True)
