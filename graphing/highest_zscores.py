import multiprocessing
import datetime
import statistics
import time

import matplotlib.pyplot as plt

import highest_zscores
from database.itemdata_operations import get_data_for_item
from database.item_operations import get_item
from settings import *

def main():
    print("Calculating Z-Scores...")
    highest_zscores_items = find_highest_zscores_items()
    return highest_zscores_items

    fig, axs = plt.subplots(len(highest_zscores))
    fig.suptitle("Z-Scores Over Time", color=FEATURE_COLOR)
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_edgecolor(FEATURE_COLOR)

    for item_index, item_data in enumerate(highest_zscores):
        item_name = item_data[ITEM_NAME]
        times = item_data[TIMESTAMP]
        scores = item_data[ZSCORES]

        axs[item_index].set_title(f"{item_name}", color=FEATURE_COLOR)
        try:
            axs[item_index].plot(times, scores,
                     marker='.',
                     linestyle='solid',
                     color=LINE_COLOR
                     )
        except Exception as e:
            print(e)
            print(item_name)
            print(times)
            print(scores)

        axs[item_index].set_xlabel(f'Times', color=FEATURE_COLOR)
        axs[item_index].set_ylabel(f'Z-Scores', color=FEATURE_COLOR)

        x_ticks = [int(x) for x in axs[item_index].get_xticks()]
        x_dates = [datetime.datetime.fromtimestamp(x) for x in x_ticks]
        x_labels = [datetime.datetime.strftime(x, "%Y%m%d\n%H:%M") for x in x_dates]

        axs[item_index].set_xticks(x_ticks, x_labels, color=FEATURE_COLOR)

        y_ticks = axs[item_index].get_yticks()
        y_labels = [f"{y:.2f}" for y in y_ticks]
        axs[item_index].set_yticks(y_ticks, y_labels, color=FEATURE_COLOR)

        axs[item_index].tick_params(which="both", labelsize="small", color=FEATURE_COLOR)

        plt.setp(axs[item_index].get_xticklabels(), rotation=30, horizontalalignment='right', color=FEATURE_COLOR)

        for score, timestamp in list(zip(scores, times)):
            axs[item_index].annotate(f"{score:.2f}",
                        xy=(timestamp, score), xycoords='data',
                        xytext=(1.5, 1.5), textcoords='offset points', color=FEATURE_COLOR)

        axs[item_index].set_facecolor(BACKGROUND_COLOR)
        for spine in axs[item_index].spines.values():
            spine.set_edgecolor(FEATURE_COLOR)

    plt.tight_layout()
    plt.show()

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
    item_progress.value += 1
    print(f"\t{time.ctime()} {item_progress.value / item_total * 100 : .0f}%", end="\r")
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