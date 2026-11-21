import concurrent.futures
import datetime
import traceback
import threading
import time

from api_calls.historical_price_volume import get_historical_price_volume
from database.item_operations import get_item, set_history_processed
from database.itemdata_operations import add_item_history
from constants import TIMESTAMP, ITEM_ID, PRICE, VOLUME, RUNESCAPE_ITEM_ID
from settings import THREAD_COUNT

ITEMS_PROCESSED = None
TOTAL_ITEMS = None
KILLED = False
LOCK = threading.Lock()

def get_historical_data():
    global ITEMS_PROCESSED, TOTAL_ITEMS, KILLED
    print("Populating historical data")

    item_history = get_historical_price_volume(2)
    timestamp = max([d[TIMESTAMP] for d in item_history[str(2)]])
    timestamp = datetime.datetime.fromtimestamp(timestamp/1000).replace(tzinfo=datetime.UTC)

    ITEMS_PROCESSED = 0
    items = get_items_needing_updates(timestamp)
    TOTAL_ITEMS = len(items)

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
         [executor.submit(update_item_id_history, item) for item in items]
    # update_item_id_history(item_ids[0])
    KILLED = True
    print()


def get_old_history_items():
    all_item_ids = get_item(expire_data=False)
    result = []
    for item in all_item_ids:
        if not item.history_processed:
            result.append(item.id)
            continue
        now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        item_timestamp = item.history_processed.replace(tzinfo=datetime.timezone.utc)
        if now - item_timestamp > datetime.timedelta(days=1):
            result.append(item.id)
    return result

def get_items_needing_updates(timestamp):
    timestamp = timestamp.replace(tzinfo=datetime.UTC)
    all_items = get_item(expire_data=False)
    all_items = [a for a in all_items if a.history_processed.replace(tzinfo=datetime.UTC) < timestamp]
    return all_items

def update_item_id_history(item):
    global ITEMS_PROCESSED
    item_history = get_historical_price_volume(item.id)
    print(f"\t{time.ctime()} Item ID: {item.name} {ITEMS_PROCESSED / TOTAL_ITEMS * 100:.2f}%", end="\r")
    if str(item.id) in item_history:
        data = item_history[str(item.id)]
        new_data = [d for d in data if
                    datetime.datetime.fromtimestamp(d[TIMESTAMP]/1000).replace(tzinfo=datetime.UTC) > item.history_processed.replace(tzinfo=datetime.UTC)]

        if not new_data:
            ITEMS_PROCESSED += 1
            return

        try:
            updates = [
                {
                    RUNESCAPE_ITEM_ID: item.id,
                    TIMESTAMP: datetime.datetime.fromtimestamp(int(d[TIMESTAMP] / 1000)).replace(tzinfo=datetime.UTC),
                    PRICE: d[PRICE],
                    VOLUME: d[VOLUME],
                 } for d in new_data
            ]
            with LOCK:
                add_item_history(item.id, updates)
                set_history_processed(item.id, datetime.datetime.utcnow())

        except Exception as exc:
            traceback.print_exc()
            print(f'{item.name} generated an exception')
            input("Paused")

    ITEMS_PROCESSED += 1

def update_status():
    while not KILLED:
        time.sleep(1)
        print(f"{time.ctime()} {ITEMS_PROCESSED / TOTAL_ITEMS * 100:.2f}%", end="\r")
    print("")

