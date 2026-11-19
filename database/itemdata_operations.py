import datetime
import time
import traceback

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from database.database import Session as GeSession, engine
from database.database import ItemData
from database.item_operations import get_item

from constants import ITEM_ID, ITEM_NAME, TIMESTAMP, PRICE, VOLUME

def add_merged_data(merged_data):
    all_items = get_item(expire_data=False)
    for item_name, item_data in merged_data.items():
        for timestamp, item_values in item_data.items():
            item_id = [item.id for item in all_items if item.name == item_name][0]
            item_values[ITEM_NAME] = item_name
            item_values[ITEM_ID] = item_id
            item_values[TIMESTAMP] = timestamp
            for d in [PRICE, VOLUME]:
                if d not in item_values:
                    item_values[d] = None
            add_latest_item_data(item_values)

def add_latest_item_data(latest_item_data):
    item_id = latest_item_data[ITEM_ID]

    timestamp = latest_item_data[TIMESTAMP]
    if not isinstance(timestamp, datetime.datetime):
        try:
            timestamp = datetime.datetime.fromisoformat(timestamp)
        except:
            timestamp = datetime.datetime.fromtimestamp(timestamp)

    price = latest_item_data[PRICE]

    volume = latest_item_data[VOLUME]

    last_update = get_last_item_data_update()
    print(f"{timestamp}\t\t{last_update}")
    if not timestamp.replace(tzinfo=datetime.timezone.utc) > last_update.replace(tzinfo=datetime.timezone.utc):
        return

    try:
        item = get_item_data(item_id, timestamp, expire_data=False)
        if item:
            update_latest_item_data(item, latest_item_data)
            return

        print("Should be adding:")
        print(latest_item_data)
        with GeSession.begin() as session:
            session.add(
                ItemData(
                    runescape_item_id=item_id,
                    timestamp=timestamp,
                    price=price,
                    volume=volume
                )
            )
            session.commit()

    except Exception as e:
        if "UNIQUE constraint failed" in traceback.format_exc():
            # print(f"Skipped adding item to database (already exists):\n\t{item_id}:{item_name}")
            return

        traceback.print_exc()
        print(f"Failed to add item to database:\n\t{item_id} at {timestamp}")


def get_item_data(item_id, timestamp, expire_data=True):
    with Session(engine, expire_on_commit=expire_data) as session:
        stmt = select(ItemData).where(ItemData.runescape_item_id == item_id, ItemData.timestamp == timestamp)
        results = session.scalars(stmt).first()
        return results

def get_data_for_item(item_id, expire_data=True):
    with Session(engine, expire_on_commit=expire_data) as session:
        stmt = select(ItemData).where(ItemData.runescape_item_id == item_id)
        results = session.scalars(stmt).all()
        return results

def update_latest_item_data(item_data, latest_item_data):
    item_id = int(latest_item_data[ITEM_ID])

    timestamp = latest_item_data[TIMESTAMP]
    timestamp = datetime.datetime.fromisoformat(timestamp)

    price = latest_item_data[PRICE]

    volume = latest_item_data[VOLUME]

    try:

        with GeSession.begin() as session:
            session.execute(update(ItemData),
                [
                    {ITEM_ID: item_data.id, PRICE: price, VOLUME: volume}
                ],
            )
            session.commit()

    except Exception as e:
            traceback.print_exc()
            print(f"Couldn't update Item ID {item_id} at {timestamp}")

def get_last_item_data_update(expire_data=False):
    with (Session(engine, expire_on_commit=expire_data) as session):
        latest_update = session.execute(func.max(ItemData.timestamp)).first()[0] or datetime.datetime.min
        return latest_update


def add_item_history(item, item_history):
    print()
    try:
        with Session(engine) as session:
            q = select(ItemData).where(ItemData.runescape_item_id == item.id)
            preexisting_items = session.scalars(q).all()
            total_items = len(item_history)
            for data_index, data in enumerate(item_history):
                try:
                    item_data = [item for item in preexisting_items if
                                 item.timestamp.replace(tzinfo=datetime.UTC) == data[TIMESTAMP].replace(tzinfo=datetime.UTC)].pop()
                    if item_data.price == data[PRICE] and item_data.volume == data[VOLUME]:
                        continue
                except IndexError:
                    item_data = ItemData(
                        runescape_item_id=item.id,
                        timestamp=data[TIMESTAMP]
                    )
                finally:
                    item_data.price = data[PRICE]
                    item_data.volume = data[VOLUME]
                    session.merge(item_data)
                    print(f"\t{time.ctime()} {(data_index+1) / total_items*100:.0f}% {item_data.runescape_item_id} {item_data.timestamp}", end="\r")
            session.commit()

    except Exception as e:
        if "UNIQUE constraint failed" in traceback.format_exc():
            print(f"Skipped adding item to database (already exists):\n\t{item.id}")
            return

        traceback.print_exc()
        print(f"Failed to add item history to database:\n\t{item.id}:{item.name}")

