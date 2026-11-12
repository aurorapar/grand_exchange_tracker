import datetime

from main import calculate_scores, load_cache
from graph_items import graph_items
from settings import *

def main():

    data = load_cache()
    target_items = TRACKED_ITEMS

    target_data = {}
    for target_item in target_items:
        try:
            test = [{k:v} for k,v in data.items() if k.lower() == target_item.lower()][0]
            target_data.update(test)
        except Exception as e:
            print(f"{target_item} is not in the cache")
            print(e)
            exit()

    graph_data = []
    calculated_scores = calculate_scores(target_data)

    for item_index, item_data in enumerate(calculated_scores):
        item_name = item_data[ITEM_NAME]
        if item_name in IGNORE_KEYS:
            continue

        x_values = item_data[TIMESTAMP]
        x_values.sort()
        y_values = item_data[ZSCORES]

        x_labels = [datetime.datetime.fromtimestamp(x) for x in x_values]
        x_labels = [datetime.datetime.strftime(x, "%Y%m%d\n%H:%M") for x in x_labels]

        y_labels = [f"{y:.2f}" for y in y_values]

        graph_data.append([item_name, [x_values, x_labels, y_values, y_labels]])

    item_names = [x[0] for x in graph_data]
    graph_data = [x[1] for x in graph_data]
    graph_items("Z-Scores Over Time", item_names, "Date", "Z-Score", graph_data)


def get_height_from_width(width):
    ratio = 6.4/4.8
    return width / ratio

if __name__ == "__main__":
    main()