import statistics
import time

from database.itemdata_operations import get_data_for_item
from database.item_operations import get_item
from settings import *

def main(lookback_date_cutoff):
    print("Calculating Z-Scores...")
    return find_highest_zscores_items(lookback_date_cutoff)

threshold_functions = THRESHOLDS


def find_highest_zscores_items(lookback_date_cutoff):
    all_items = get_item(expire_data=False)
    item_total = len(all_items)

    with multiprocessing.Manager() as manager:
        with multiprocessing.Pool(THREAD_COUNT) as pool:
            highest_zscores_items = []
            results = manager.dict()
            item_progress = manager.Value('i', 0)
            passes = manager.dict({
                "too_old": 0,
                "no_price_volume": 0,
                "below_threshold": 0,
                "std_dev": 0,
            })

            # test 1 item
            # calculate_zscore([results, lookback_date_cutoff, all_items[0].id, item_progress, item_total])
            # test all items
            pool.map(calculate_zscore, [(results, lookback_date_cutoff, item.id, item_progress, item_total, passes) for item in all_items])

            for item_id, zscore in results.items():

                if len(highest_zscores_items) < NUMBER_OF_ITEMS_TO_GRAPH:
                    highest_zscores_items.append((item_id, zscore))
                    highest_zscores_items = sorted(highest_zscores_items, key=lambda x: x[1])
                    continue

                lowest_zscore = highest_zscores_items[0][1]
                if highest_zscores_items[0][1] < zscore:
                    highest_zscores_items = [(item_id, zscore)] + highest_zscores_items[1:]
                    highest_zscores_items = sorted(highest_zscores_items, key=lambda x: x[1])
        print()
        # print(f"{passes}")
    return highest_zscores_items

def calculate_zscore(data):
    global DATA_TOO_OLD_COUNT, NO_PRICE_OR_VOLUME_DATA, BELOW_THRESHOLD, STD_DEV_ZERO
    results = data[0]
    lookback_date_cutoff = data[1]
    item_id = data[2]
    item_progress = data[3]
    item_total = data[4]
    passes = data[5]
    item_data = get_data_for_item(item_id=item_id, expire_data=False)
    item_data = [d for d in item_data if d.timestamp.replace(tzinfo=datetime.UTC) > lookback_date_cutoff]
    item_progress.value += 1
    print(f"\t{time.ctime()} {item_progress.value / item_total * 100 : .0f}%", end="\r")

    if not item_data:
        results[item_id] = 0
        passes["too_old"] += 1
        return

    item_data = [data_point for data_point in item_data
                 if (data_point.price or data_point.average_high)
                 and (data_point.volume or data_point.high_price_volume)
    ]
    item_data.sort(key=lambda x: x.timestamp)
    if not item_data or len(item_data) < 2:
        results[item_id] = 0
        passes["no_price_volume"] += 1
        return
    prices = [d.price or d.average_high for d in item_data]
    volumes = [d.volume or d.high_price_volume for d in item_data]
    average_price = statistics.mean(prices)
    average_volume = statistics.mean(volumes)

    for threshold_check in threshold_functions:
        if threshold_check(average_price, average_volume):
            results[item_id] = 0
            passes["below_threshold"] += 1
            return

    newest_point = item_data[-1]

    s = statistics.stdev(prices)
    if s == 0:
        passes["std_dev"] += 1
        results[item_id] = 0
        return

    m = statistics.mean(prices)
    zscore = abs(((newest_point.price or newest_point.average_high) - m) / s)
    results[item_id] = zscore


if __name__ == "__main__":
    main()