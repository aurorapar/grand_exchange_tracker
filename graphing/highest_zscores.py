import datetime
import statistics
import time

from database.itemdata_operations import get_data_for_item
from database.item_operations import get_item
from settings import *

def main(lookback_date_cutoff):
    print("Calculating Z-Scores...")
    return find_highest_zscores_items(lookback_date_cutoff)

threshold_functions = THRESHOLDS
threshold_sample_points = THRESHOLD_SAMPLE_POINTS

def find_highest_zscores_items(lookback_date_cutoff):
    all_items = get_item(expire_data=False)
    item_total = len(all_items)
    highest_zscores_items = []

    with multiprocessing.Manager() as manager:
        with multiprocessing.Pool(THREAD_COUNT) as pool:
            results = manager.dict()
            item_progress = manager.Value('i', 0)
            pool.map(calculate_zscore, [(results, lookback_date_cutoff, item.id, item_progress, item_total) for item in all_items])

            for item_id, zscore in results.items():

                if not zscore:
                    continue
                if len(highest_zscores_items) < NUMBER_OF_ITEMS_TO_GRAPH:
                    highest_zscores_items.append((item_id, zscore))
                    highest_zscores_items = sorted(highest_zscores_items, key=lambda x: x[1])
                    continue

                if highest_zscores_items[0][1] < zscore:
                    highest_zscores_items = [(item_id, zscore)] + highest_zscores_items[1:]
                    highest_zscores_items = sorted(highest_zscores_items, key=lambda x: x[1])
    print()
    return highest_zscores_items

def calculate_zscore(data):
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

    item_data = [data_point for data_point in item_data if data_point.price and data_point.volume] # [:number_of_last_points]]
    item_data.sort(key=lambda x: x.timestamp)
    if not item_data or len(item_data) < 2:
        results[item_id] = 0
        return
    prices = [d.price for d in item_data]
    volumes = [d.volume for d in item_data]
    average_price = statistics.mean(prices)
    average_volume = statistics.mean(volumes)

    for threshold_check in threshold_functions:
        if threshold_check(average_price, average_volume):
            results[item_id] = 0
            return

    newest_point = item_data[-1]

    s = statistics.stdev(prices)
    if s == 0:
        results[item_id] = 0
        return

    m = statistics.mean(prices)
    zscore = (newest_point.price - m) / s

    results[item_id] = zscore


if __name__ == "__main__":
    main()