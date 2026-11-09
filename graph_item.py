import datetime
import json
import os

import matplotlib.pyplot as plt

DATA_STORE_FILE = "prices.json"
DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), DATA_STORE_FILE)

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

    # width = 3
    # height = get_height_from_width(width)
    fig, axs = plt.subplots(len(target_data))
    fig.suptitle("Item Prices Over Time")

    for item_index, item_data in enumerate(target_data):
        item_name = list(item_data.keys())[0]
        time_stamps = [int(x) for x in item_data[item_name].keys()]
        time_stamps.sort()
        prices = [int(item_data[item_name][str(t)]) for t in time_stamps]


        axs[item_index].set_title(f"{item_name}")
        axs[item_index].plot(time_stamps, prices,
                 marker='.',
                 linestyle='solid'
                 )

        axs[item_index].set_xlabel(f'Times')
        axs[item_index].set_ylabel('Prices')

        xlabels = time_stamps
        xlabels = [datetime.datetime.fromtimestamp(x) for x in xlabels]
        xlabels = [datetime.datetime.strftime(x, "%Y%m%d\n%H:%M") for x in xlabels]
        # axs[item_index].xticks(time_stamps, xlabels)
        axs[item_index].tick_params("x", labelsize="small")
        axs[item_index].set_xticks(time_stamps, xlabels)
        plt.setp(axs[item_index].get_xticklabels(), rotation=30, horizontalalignment='right')


    # plt.margins(.02)
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