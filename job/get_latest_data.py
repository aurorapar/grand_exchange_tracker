import datetime
import time
import traceback

from api_calls.five_minute import main as get_latest_data
from database.database import ItemData
from database.item_operations import set_history_processed
from database.itemdata_operations import add_new_itemdatas
from job.old_data_items import get_old_history_items
from constants import TIMESTAMP, DATA,  AVG_HIGH, AVG_LOW, HIGH_PRICE_VOLUME, LOW_PRICE_VOLUME


def main(thread_lock):
    print(f"Updating latest data...")

    data = get_latest_data()
    timestamp = datetime.datetime.fromtimestamp(data[TIMESTAMP], datetime.UTC)
    data = data[DATA]

    items_needing_updates = [(item, data[str(item.id)] )for item in get_old_history_items(timestamp) if str(item.id) in data]
    total_items = len(items_needing_updates)
    print(f"\tItems needing processed: {total_items}")
    items_processed = 0
    new_items = []

    for update_item in items_needing_updates:
        item = update_item[0]
        item_data = update_item[1]
        try:
            update = ItemData(
                runescape_item_id=item.id,
                timestamp=timestamp,
                average_high=item_data[AVG_HIGH],
                average_low=item_data[AVG_LOW],
                high_price_volume=item_data[HIGH_PRICE_VOLUME],
                low_price_volume=item_data[LOW_PRICE_VOLUME]
            )
            with thread_lock:
                new_items.append(update)
        except:
            traceback.print_exc()
            input(item_data)
        finally:
            items_processed += 1
            print(f"\t{time.ctime()} Items Processed: {items_processed / total_items * 100:.2f}%", end="\r")
    add_new_itemdatas(new_items)
    for update_item in items_needing_updates:
        with thread_lock:
            set_history_processed(update_item[0].id, timestamp)


