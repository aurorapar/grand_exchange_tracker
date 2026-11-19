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
        data_for_item.sort(key=lambda x: x.timestamp)
        if not data_for_item:
            print(f"No data for {item.name}???")
            print(data_for_item)
            continue

        x_values = [d.timestamp for d in data_for_item]
        x_labels = [datetime.datetime.strftime(d, "%Y%m%d") for d in x_values]

        y_values = [(d.price, d.volume) for d in data_for_item]
        y_labels = y_values

        graph_data.append([f"{item_name}    Z:{zscore:.2f}", [x_values, x_labels, y_values, y_labels]])

    print("Data Prepared. Starting graphing")
    graph_data = graph_data[::-1]
    item_names = [x[0] for x in graph_data]
    graph_data = [x[1] for x in graph_data]
    graph_items(f"{NUMBER_OF_ITEMS_TO_GRAPH} Items With Highest Z-Scores\nSince {datetime.datetime.utcnow() - datetime.timedelta(days=LOOKBACK_DAYS)}",
                item_names, "Date", ["Price", "Volume"], graph_data)



if __name__ == "__main__":
    main()