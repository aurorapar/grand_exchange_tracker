import datetime
import statistics

from database.item_operations import get_item
from database.itemdata_operations import get_data_for_item
from graphing.graph_items import graph_items

from settings import *


def main(zscore_items, lookback_date_cutoff):
    print("Preparing graph data")
    graph_data = []

    for scores in zscore_items:
        item_id = scores[0]
        zscore = scores[1]
        item = get_item(item_id, expire_data=False).pop()
        item_name = item.name

        data_for_item = get_data_for_item(item_id, expire_data=False)
        data_for_item = [d for d in data_for_item if d.timestamp.replace(tzinfo=datetime.UTC) > lookback_date_cutoff]
        if not data_for_item:
            print(f"No data for {item.name}???")
            print(data_for_item)
            continue
        desired_data = [(item_data.timestamp, item_data.price) for item_data in data_for_item]
        desired_data = sorted(desired_data, key=lambda x: x[0])
        volumes = [item_data.volume or 0 for item_data in data_for_item[:min(len(data_for_item), THRESHOLD_SAMPLE_POINTS) * -1]]
        average_volume = statistics.mean(volumes) if volumes else 0

        x_values = [d[0].timestamp() for d in desired_data]
        x_labels = [datetime.datetime.strftime(d[0], "%Y%m%d") for d in desired_data]

        y_values = [d[1] for d in desired_data]
        y_labels = [f"{y:.2f}" for y in y_values]

        graph_data.append([f"{item_name}    Z:{zscore:.2f}    Avg Vol: {int(average_volume)}", [x_values, x_labels, y_values, y_labels]])

    print("Data Prepared. Starting graphing")
    graph_data = graph_data[::-1]
    item_names = [x[0] for x in graph_data]
    graph_data = [x[1] for x in graph_data]
    graph_items(f"{NUMBER_OF_ZSCORES} Items With Highest Z-Scores\nSince {datetime.datetime.utcnow() - datetime.timedelta(days=DAYS_PAST_TO_GRAPH)}", item_names, "Date", "Price", graph_data)



if __name__ == "__main__":
    main()