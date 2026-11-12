import datetime
import json
import statistics

import matplotlib.pyplot as plt

from settings import *

def main():

    data = load_cache()
    highest_zscores = []

    for item_name, item_data in data.items():
        if item_name in IGNORE_KEYS:
            continue
        zscore = {
            ITEM_NAME: item_name,
            TIMESTAMP: [],
            ZSCORES: [],
            ZSCORE_DEV: None
        }

        item_scores = sorted([(int(t),int(s)) for t, s in item_data.items()], key=lambda x:x[0])
        for index in range(len(item_scores) + 1):
            if index < 2:
                continue
            sub_prices = [x[1] for x in item_scores][:index]
            time_stamp = [x[0] for x in item_scores][:index][-1]
            price = sub_prices[-1]

            s = statistics.stdev(sub_prices)
            if s == 0:
                zscore[ZSCORES].append(s)
            else:
                m = statistics.mean(sub_prices)
                zscore[ZSCORES].append((price - m) / s)
            zscore[TIMESTAMP].append(time_stamp)

        try:
            zscore[ZSCORE_DEV] = statistics.stdev(zscore[ZSCORES])
        except Exception as e:
            print(f"Error trying to parse data for {item_name}, skipping")
            print(f"\tValues: {zscore[TIMESTAMP]} {zscore[ZSCORES]}")
            print(e)
            continue

        if len(highest_zscores) < NUMBER_OF_ZSCORES:
            highest_zscores.append(zscore)
            highest_zscores.sort(key=lambda x: x[ZSCORE_DEV])
            continue

        if zscore[ZSCORE_DEV] > highest_zscores[0][ZSCORE_DEV]:
            highest_zscores[0] = zscore
            highest_zscores.sort(key=lambda x: x[ZSCORE_DEV])

    if not highest_zscores:
        print("Not enough data to graph")
        exit()

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

def load_cache():
    try:
        with open(DATA_STORE_FILE, "r") as f:
            data = json.load(f)
            print("Cache loaded")
    except Exception as e:
        print("Error loading cache:", e)
        exit()

    return data

def get_height_from_width(width):
    ratio = 6.4/4.8
    return width / ratio

if __name__ == "__main__":
    main()