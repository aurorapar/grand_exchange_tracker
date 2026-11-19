import datetime
import multiprocessing
import threading
import time

from api_calls.latest import get_latest_data
from api_calls.mapping import get_mapping_data
from api_calls.prices_volume_merge import get_prices_volume_merged
from database.database import main as initialize_database
from database.item_operations import add_mapping_data, get_item
from database.itemdata_operations import add_latest_item_data, add_merged_data
from graphing.highest_zscores import main as get_highest_zscores
from graphing.graph_zscore_items import main as graph_zscore_items
from job.get_historical_data import get_historical_data
from settings import LOOKBACK_DAYS


def main():
    initialize_database()
    add_items_from_mappings()
    get_historical_data()

    lookback_date_cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=LOOKBACK_DAYS)
    zscores = get_highest_zscores(lookback_date_cutoff)
    display_multiple_graphs(lookback_date_cutoff, zscores)


def add_items_from_mappings():
    # using a method so that memory can be garbage collected
    print("Getting Mapping data from api")
    mapping_data = get_mapping_data()
    print("Storing Mapping data in database")
    add_mapping_data(mapping_data)

def add_latest_data():
    print("Getting Items from database")
    items = get_item(expire_data=False)

    print("Getting Item data from api")
    item_total = len(items)
    item_count = 0

    while item_count < item_total:
        queried_items = items[:min(100, len(items))]
        add_latest_items_data(queried_items)
        item_count += 100
        print(f"\t{item_count/item_total*100:.0f}%", end="\r")
        items = items[min(100, len(items)):]
    print("")


def add_latest_items_data(items):
    latest_items_data = get_latest_data(items)
    for latest_item_data in latest_items_data.values():
        add_latest_item_data(latest_item_data)


def add_price_volume():
    print("Getting Merged Price And Volume from api")
    merged_data = get_prices_volume_merged()
    print("Storing Merged Price And Volume in database")
    add_merged_data(merged_data)


def display_multiple_graphs(lookback_date, zscores):
    display_thread = threading.Thread(target=graph_zscore, args=(lookback_date, zscores))
    display_thread.start()
    while True:
        time.sleep(1)

def graph_zscore(lookback_date, zscores):
    procs = []
    for zscore in zscores:
        proc = multiprocessing.Process(target=graph_zscore_items, args=([zscore], lookback_date))
        proc.start()
        procs.append(proc)
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    main()