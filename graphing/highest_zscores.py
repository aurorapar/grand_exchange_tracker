import statistics
import time

from database.itemdata_operations import get_data_for_item
from database.item_operations import get_item
from settings import *

def main():
    print("Calculating Z-Scores...")
    return find_highest_zscores_items()

threshold_functions = THRESHOLDS
threshold_sample_points = THRESHOLD_SAMPLE_POINTS

def find_highest_zscores_items():
    all_items = get_item(expire_data=False)
    item_total = len(all_items)
    highest_zscores_items = []

    with multiprocessing.Manager() as manager:
        with multiprocessing.Pool(THREAD_COUNT) as pool:
            results = manager.dict()
            item_progress = manager.Value('i', 0)
            pool.map(calculate_zscore, [(results, item.id, item_progress, item_total) for item in all_items])

            for item_id, zscore in results.items():

                if not zscore:
                    continue
                if len(highest_zscores_items) < NUMBER_OF_ZSCORES:
                    highest_zscores_items.append((item_id, zscore))
                    highest_zscores_items = sorted(highest_zscores_items, key=lambda x: x[1])
                    continue

                if highest_zscores_items[0][1] < zscore:
                    highest_zscores_items = [(item_id, zscore)] + highest_zscores_items[1:]
                    highest_zscores_items = sorted(highest_zscores_items, key=lambda x: x[1])
    return highest_zscores_items

def calculate_zscore(data):
    results = data[0]
    item_id = data[1]
    item_progress = data[2]
    item_total = data[3]
    item_data = get_data_for_item(item_id=item_id, expire_data=False)
    if not item_data:
        results[item_id] = None
        return
    item_progress.value += 1
    print(f"\t{time.ctime()} {item_progress.value / item_total * 100 : .0f}%", end="\r")

    threshold_points = [data_point for data_point in item_data[:min(len(item_data), threshold_sample_points) * -1]]
    newest_prices = [d.price or 0 for d in threshold_points]
    newest_volumes = [d.volume or 0 for d in threshold_points]
    if newest_volumes and newest_volumes:
        average_price = statistics.mean(newest_prices)
        average_volume = statistics.mean(newest_volumes)

        for threshold_check in threshold_functions:
            if threshold_check(average_price, average_volume):
                results[item_id] = None
                return

    prices = [data_point.price for data_point in item_data]
    if len(prices) < 2:
        results[item_id] = None
        return
    max_timestamp = max(data_point.timestamp for data_point in item_data)
    newest_point = [data_point for data_point in item_data if data_point.timestamp == max_timestamp][0]

    s = statistics.stdev(prices)
    if s == 0:
        results[item_id] = 0
        return

    m = statistics.mean(prices)
    zscore = (newest_point.price - m) / s

    results[item_id] = zscore

def get_height_from_width(width):
    ratio = 6.4/4.8
    return width / ratio

if __name__ == "__main__":
    main()