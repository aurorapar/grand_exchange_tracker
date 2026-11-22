import datetime
import statistics
import time

from database.itemdata_operations import get_data_for_item
from database.item_operations import get_item
from settings import *

def main(lookback_date_cutoff):
    print("Finding volumes...")
    return find_highest_volume_items(lookback_date_cutoff)

threshold_functions = THRESHOLDS

def find_highest_volume_items(lookback_date_cutoff):
    all_items = get_item(expire_data=False)
    item_total = len(all_items)
    highest_volume_items = []

    with multiprocessing.Manager() as manager:
        with multiprocessing.Pool(THREAD_COUNT) as pool:
            results = manager.dict()
            item_progress = manager.Value('i', 0)
            pool.map(calculate_volume, [(results, lookback_date_cutoff, item.id, item_progress, item_total) for item in all_items])

            for item_id, v in results.items():

                if len(highest_volume_items) < NUMBER_OF_ITEMS_TO_GRAPH:
                    highest_volume_items.append((item_id, v))
                    highest_volume_items = sorted(highest_volume_items, key=lambda x: x[1])
                    continue

                if highest_volume_items[0][1] < v:
                    highest_volume_items = [(item_id, v)] + highest_volume_items[1:]
                    highest_volume_items = sorted(highest_volume_items, key=lambda x: x[1])
    print()
    return highest_volume_items

def calculate_volume(data):
    results = data[0]
    lookback_date_cutoff = data[1]
    item_id = data[2]
    item_progress = data[3]
    item_total = data[4]
    item_data = get_data_for_item(item_id=item_id, expire_data=False)
    item_data = [d for d in item_data if d.timestamp.replace(tzinfo=datetime.UTC) > lookback_date_cutoff]
    item_progress.value += 1
    print(f"\t{time.ctime()} {item_progress.value / item_total * 100 : .0f}%", end="\r")

    if not item_data:
        results[item_id] = 0
        return

    threshold_points = [data_point for data_point in item_data]
    newest_prices = [d.price or 0 for d in threshold_points]
    newest_volumes = [d.volume or 0 for d in threshold_points]
    if newest_volumes and newest_volumes:
        average_price = statistics.mean(newest_prices)
        average_volume = statistics.mean(newest_volumes)

        for threshold_check in threshold_functions:
            if threshold_check(average_price, average_volume):
                results[item_id] = 0
                return

    volumes = [data_point.volume or 0 for data_point in item_data]
    volume = sum(volumes)
    results[item_id] = volume


if __name__ == "__main__":
    main()