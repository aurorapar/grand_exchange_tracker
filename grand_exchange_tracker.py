import datetime
import multiprocessing
import subprocess
import threading
import time

import shopen

from api_calls.mapping import get_mapping_data
from database.database import main as initialize_database
from database.item_operations import add_mapping_data, get_item
from job.get_historical_data import get_historical_data
from job.get_latest_data import main as import_latest_data

from graphing.highest_zscores import main as get_highest_zscores
from graphing.highest_volumes import main as get_highest_volumes
from graphing.graph_zscore_items import main as graph_zscore_items
from graphing.graph_volume_items import main as graph_volume_items

# from constants import DISPLAY_FILE
from settings import LOOKBACK_DAYS

LOCK = threading.Lock()

def main():
    lookback_date_cutoff = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=LOOKBACK_DAYS)

    initialize_database()
    initialize_threads()

    # volumes = get_highest_volumes(lookback_date_cutoff)

    zscores = get_highest_zscores(lookback_date_cutoff)
    # input(zscores)
    # zscores = [(30066, 3.9659907955569667), (25454, 4.052224174983592), (23953, 4.154987422326744), (12484, 4.198585973713432), (9338, 4.341873031380608), (28313, 4.527244870157542), (30848, 7.211750536062137), (10145, 9.592217590206781)]
    display_multiple_graphs(lookback_date_cutoff, zscores)

def initialize_threads():
    # mapping_thread = threading.Thread(target=add_items_from_mappings, args=(LOCK,), daemon=True)
    # latest_data_thread = threading.Thread(target=add_latest_data, args=(LOCK,),  daemon=True)
    # historical_thread = threading.Thread(target=add_historical_data, args=(LOCK,), daemon=True)
    #
    # for t in [mapping_thread, latest_data_thread, historical_thread]:
    #     t.start()

    print("Getting Mapping data from api")
    mapping_data = get_mapping_data()
    print("Storing Mapping data in database")
    add_mapping_data(mapping_data, LOCK)

    import_latest_data(LOCK)

    get_historical_data(LOCK)

def add_items_from_mappings(thread_lock):
    while True:
        # using a method so that memory can be garbage collected
        print("Getting Mapping data from api")
        mapping_data = get_mapping_data()
        print("Storing Mapping data in database")
        add_mapping_data(mapping_data, thread_lock)
        time.sleep(60 * 60 * 24)


def add_latest_data(thread_lock):
   while True:
        import_latest_data(thread_lock)
        time.sleep(300)

def add_historical_data(thread_lock):
    while True:
        get_historical_data(thread_lock)
        time.sleep(60*60*3)

def display_multiple_graphs(lookback_date, zscores):
    display_thread = threading.Thread(target=graph_via_process, args=(lookback_date, zscores))
    display_thread.start()
    while True:
        time.sleep(1)

def graph_via_process(lookback_date, metrics):
    procs = []
    for metric in metrics:
        proc = multiprocessing.Process(target=graph_zscore_items, args=([metric], lookback_date))
        proc.start()
        procs.append(proc)
    for proc in procs:
        proc.join()

if __name__ == "__main__":
    main()