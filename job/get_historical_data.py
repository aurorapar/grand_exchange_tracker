import concurrent.futures
import datetime
import traceback
import threading
import time

from api_calls.historical_price_volume import get_historical_price_volume
from database.item_operations import get_item, set_history_processed
from database.itemdata_operations import add_item_history
from constants import TIMESTAMP, PRICE, VOLUME, RUNESCAPE_ITEM_ID
from settings import THREAD_COUNT, API_REFRESH

KILLED = False
LOCK = threading.Lock()

def get_historical_data():
    print("Populating historical data")

    items = get_old_history_items()
    if not items:
        print("\tHave recent data, skipping")
        return
    items_processed = 0
    total_items = len(items)
    print(f"{total_items} items need updating")
    print("\t(If some items need updating every time, there has been no market data for them recently)")
    sleep_time = 0
    # for item in items:
    #     update_item_id_history(item, sleep_time, items_processed, total_items)
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
       [executor.submit(update_item_id_history, item, sleep_time, items_processed, total_items) for item in items]
    update_item_id_history(items[0], sleep_time, items_processed, total_items)
    print()


def get_old_history_items():
    all_item_ids = get_item(expire_data=False)
    result = []
    for item in all_item_ids:
        if not item.history_processed:
            result.append(item)
            continue
        now = datetime.datetime.now().replace(tzinfo=datetime.UTC)
        item_timestamp = item.history_processed.replace(tzinfo=datetime.UTC)
        if now - item_timestamp > API_REFRESH:
            result.append(item)
    return result

def update_item_id_history(item, sleep_time, items_processed, total_items):
    item_history = get_historical_price_volume(item.id, sleep_time)
    if str(item.id) in item_history:
        item_history = item_history[str(item.id)]
        max_timestamp = max([d[TIMESTAMP] for d in item_history])
        max_timestamp = datetime.datetime.fromtimestamp(max_timestamp / 1000)
        item_history = [h for h in item_history if not item.history_processed or
                        datetime.datetime.fromtimestamp(h[TIMESTAMP] / 1000).replace(
                            tzinfo=datetime.UTC) > item.history_processed.replace(tzinfo=datetime.UTC)]

        if not item_history:
            items_processed += 1
            print(f"\t{time.ctime()} Item: {item.name} {items_processed / total_items * 100:.2f}% {' ' * 20 }", end="\r")
            return
        new_points_count = len(item_history)
        print(f"\t{time.ctime()} Item: {item.name} {items_processed / total_items * 100:.2f}% ({new_points_count} new prices) {' ' * 20 }", end="\r")

        try:

            updates = [
                {
                    RUNESCAPE_ITEM_ID: item.id,
                    TIMESTAMP: datetime.datetime.fromtimestamp(int(data_piece[TIMESTAMP] / 1000)),
                    PRICE: data_piece[PRICE],
                    VOLUME: data_piece[VOLUME],
                 } for data_piece in item_history
            ]

            add_item_history(item, updates)
            set_history_processed(item.id, max_timestamp)
            items_processed += 1

        except Exception as exc:
            traceback.print_exc()
            print(f'{item.id} generated an exception')
            input("Paused")

