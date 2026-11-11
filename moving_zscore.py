import datetime
import json
import os
import statistics

import matplotlib.pyplot as plt

DATA_STORE_FILE = "prices.json"
DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), DATA_STORE_FILE)
PINK = (1,0,150/255)
BLACK = (0,0,0)

def main():

    data = load_cache()
    target_items = ["3rd Age druidic cloak", "Accursed sceptre (au)"]

    target_data = []
    for target_item in target_items:
        test = [{k:v} for k,v in data.items() if k.lower() == target_item.lower()]
        if not test:
            print(f"{target_item} is not in the cache")
            exit()
        for t in test:
            target_data.append(t)

    fig, axs = plt.subplots(len(target_data))
    fig.suptitle("Z-Scores Over Time", color=PINK)
    fig.set_facecolor(BLACK)
    fig.set_edgecolor(PINK)

    for item_index, item_data in enumerate(target_data):
        item_name = list(item_data.keys())[0]
        time_stamps = [int(x) for x in item_data[item_name].keys()]
        time_stamps.sort()
        prices = [int(item_data[item_name][str(t)]) for t in time_stamps]

        price_data = list(zip(time_stamps, prices))
        z_scores = []

        for index in range(len(price_data) + 1):
            if index < 2:
                continue
            sub_prices = price_data[:index]
            time_stamp = sub_prices[-1][0]
            price = sub_prices[-1][1]

            s = statistics.stdev([x[1] for x in sub_prices])
            if s == 0:
                z_scores.append((time_stamp, s))
            else:
                m = statistics.mean([x[1] for x in sub_prices])
                z_scores.append((time_stamp, (price - m) / s))

        if not z_scores:
            print("Not enough data to graph")
            exit()

        times = [x[0] for x in z_scores]
        scores = [x[1] for x in z_scores]

        axs[item_index].set_title(f"{item_name}")
        axs[item_index].plot(times, scores,
                 marker='.',
                 linestyle='solid'
                 )

        axs[item_index].set_xlabel(f'Times', color=PINK)
        axs[item_index].set_ylabel(f'Z-Scores', color=PINK)

        xlabels = times
        xlabels = [datetime.datetime.fromtimestamp(x) for x in xlabels]
        xlabels = [datetime.datetime.strftime(x, "%Y%m%d\n%H:%M") for x in xlabels]

        #axs[item_index].tick_params("y", color=PINK)
        axs[item_index].set_xticks(times, xlabels, color=PINK)
        axs[item_index].tick_params(which="both", labelsize="small", color=PINK)

        #axs[item_index].set_yticks(scores, scores, color=PINK)
        plt.setp(axs[item_index].get_xticklabels(), rotation=30, horizontalalignment='right', color=PINK)

        axs[item_index].set_facecolor(BLACK)
        for spine in axs[item_index].spines.values():
            spine.set_edgecolor(PINK)

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