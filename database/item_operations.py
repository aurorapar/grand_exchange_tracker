import traceback

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import Session as GeSession, engine
from database.database import RunescapeItem

from constants import ITEM_ID, ITEM_NAME

def add_item_from_mapping(item_mapping_data):
    item_name = item_mapping_data[ITEM_NAME]
    item_id = item_mapping_data[ITEM_ID]
    try:
        item = get_item(item_id, expire_data=False)
        if item:
            return
        with GeSession.begin() as session:
            session.add(
                RunescapeItem(
                    id=item_id,
                    name=item_name
                )
            )

    except Exception as e:
        if "UNIQUE constraint failed" in traceback.format_exc():
            # Skip adding item to database (already exists)
            return

        traceback.print_exc()
        print(f"Failed to add item to database:\n\t{item_id}:{item_name}")


def add_mapping_data(mapping_data):
    item_count = len(mapping_data)
    for item_index, item in enumerate(mapping_data):
        add_item_from_mapping(item)
        print(f"\t{item_index / item_count * 100:.0f}%", end="\r")
    print("")

def get_item(item_id=None, expire_data=True):
    with Session(engine, expire_on_commit=expire_data) as session:

        if not item_id:
            stmt = select(RunescapeItem)
        else:
            stmt = select(RunescapeItem).where(RunescapeItem.id == item_id)

        results = session.scalars(stmt).all()
        return results

def set_history_processed(item_id, value):
    with Session(engine) as session:
        try:
            stmt = select(RunescapeItem).where(RunescapeItem.id == item_id)
            item = session.scalars(stmt).one()
            item.history_processed = value
            session.commit()
        except Exception as e:
            print(e)
            input("Pasused")
