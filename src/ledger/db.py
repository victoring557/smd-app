"""The database: its tables and the connection to it."""

import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, String, create_engine, event
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)
from sqlalchemy.types import TypeDecorator

DATABASE_URL = "sqlite:///ledger.db"


class Money(TypeDecorator):
    """An amount: a Decimal in Python, a whole number of cents in the database."""

    impl = Integer
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        cents = value * 100
        if cents != cents.to_integral_value():
            raise ValueError(f"{value} has fractions of a cent")
        return int(cents)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return Decimal(value).scaleb(-2)


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    rows: Mapped[list[TransactionRow]] = relationship(back_populates="account")


class TransactionRow(Base):
    """One row of the table `transactions`."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date]
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    description: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50))
    amount: Mapped[Decimal] = mapped_column(Money)

    account: Mapped[Account] = relationship(back_populates="rows")


engine = create_engine(DATABASE_URL)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    """SQLite checks foreign keys only when asked to, once per connection."""
    dbapi_connection.execute("PRAGMA foreign_keys = ON")


def create_tables() -> None:
    """Creates the tables that don't exist yet. Existing tables are not changed."""
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
