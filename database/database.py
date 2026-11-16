import datetime
import traceback

import sqlalchemy as sql
from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker

from constants import *
from main import load_cache

if not os.path.exists(DATABASE_FILE):
    try:
        os.makedirs(os.path.dirname(DATABASE_FILE))
    except FileExistsError:
        pass
    with open(DATABASE_FILE, "w") as f:
        pass

engine = sql.create_engine("sqlite:///" + DATABASE_FILE)
Session = sessionmaker(engine)

def main():
    initialize_database()

def initialize_database():
    Base.metadata.create_all(engine)

class Base(DeclarativeBase):
    pass

class RunescapeItem(Base):
    __tablename__ = "runescape_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class ItemData(Base):
    __tablename__ = "item_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    runescape_item_id: Mapped[int] = mapped_column(ForeignKey("runescape_item.id"))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    volume: Mapped[int] = mapped_column(Integer, nullable=True)

    price: Mapped[int] = mapped_column(Integer, nullable=True)
    daily_average: Mapped[int] = mapped_column(Integer, nullable=True)
    average_high: Mapped[int] = mapped_column(Integer, nullable=True)
    average_low: Mapped[int] = mapped_column(Integer, nullable=True)
    high_price_volume: Mapped[int] = mapped_column(Integer, nullable=True)
    low_price_volume: Mapped[int] = mapped_column(Integer, nullable=True)

if __name__ == "__main__":
    main()
