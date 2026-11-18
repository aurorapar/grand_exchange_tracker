import datetime
import statistics
from math import ceil

from database.item_operations import get_item
from database.itemdata_operations import get_data_for_item
from graphing.graph_items import graph_items

from settings import *


def main(zscore_items):
    graph_data = []

    for scores in zscore_items:
        item_id = scores[0]
        zscore = scores[1]
        item = get_item(item_id, expire_data=False).pop()
        item_name = item.name

        data_for_item = get_data_for_item(item_id, expire_data=False)
        desired_data = [(item_data.timestamp, item_data.price) for item_data in data_for_item]
        desired_data = sorted(desired_data, key=lambda x: x[0])
        volumes = [item_data.volume or 0 for item_data in data_for_item[:min(len(data_for_item), THRESHOLD_SAMPLE_POINTS) * -1]]
        average_volume = statistics.mean(volumes)

        x_values = [d[0].timestamp() for d in desired_data]
        x_labels = [datetime.datetime.strftime(d[0], "%Y%m%d\n%H:%M") for d in desired_data]

        y_values = [d[1] for d in desired_data]
        y_labels = [f"{y:.2f}" for y in y_values]

        graph_data.append([f"{item_name} Z:{zscore:.2f} Average Volume: {int(average_volume)}", [x_values, x_labels, y_values, y_labels]])

    graph_data = graph_data[::-1]
    item_names = [x[0] for x in graph_data]
    graph_data = [x[1] for x in graph_data]
    graph_items("Items With Highest Z-Scores", item_names, "Date", "Price", graph_data)



if __name__ == "__main__":
    main()