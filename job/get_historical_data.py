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

    ITEMS_PROCESSED = 0
    item_ids = get_old_history_items()
    TOTAL_ITEMS = len(item_ids)

    #t = threading.Thread(target=update_status)
    #t.start()
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
         [executor.submit(update_item_id_history, item_id) for item_id in item_ids]
    update_item_id_history(item_ids[0])
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

def update_item_id_history(item_id):
    global ITEMS_PROCESSED
    item_history = get_historical_price_volume(item_id)
    print(f"{time.ctime()} Item ID: {item_id} {ITEMS_PROCESSED / TOTAL_ITEMS * 100:.2f}%", end="\r")
    if str(item_id) in item_history:
        data = item_history[str(item_id)]
        max_timestamp = max([d[TIMESTAMP] for d in data])
        max_timestamp = datetime.datetime.fromtimestamp(max_timestamp/1000)

        now = datetime.datetime.now()
        if now- max_timestamp > datetime.timedelta(days=30):
            return

        data_length = len(data)

        try:
            updates = [
                {
                    RUNESCAPE_ITEM_ID: item_id,
                    TIMESTAMP: datetime.datetime.fromtimestamp(int(data_piece[TIMESTAMP] / 1000)),
                    PRICE: data_piece[PRICE],
                    VOLUME: data_piece[VOLUME],
                 } for data_piece in data
            ]
            with LOCK:
                add_item_history(item_id, updates)
                set_history_processed(item_id, now)

        except Exception as exc:
            traceback.print_exc()
            print(f'{item_id} generated an exception')
            input("Paused")

        # print(f"Item {data_index/data_length*100:.0f}%", end="\r")
        # print(f"Total {future_index / item_count*100:.0f}%", end="\r")

    ITEMS_PROCESSED += 1

def update_status():
    while not KILLED:
        time.sleep(1)
        print(f"{time.ctime()} {ITEMS_PROCESSED / TOTAL_ITEMS * 100:.2f}%", end="\r")
    print("")

