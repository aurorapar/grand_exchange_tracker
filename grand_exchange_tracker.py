import subprocess
import threading
import time

import shopen

from api_calls.mapping import get_mapping_data
from database.database import main as initialize_database
from database.item_operations import add_mapping_data, get_item
from job.get_historical_data import get_historical_data
from job.get_latest_data import main as import_latest_data

from constants import DISPLAY_FILE

LOCK = threading.Lock()

def main():
    initialize_database()
    # initialize_threads()
    shopen.open(DISPLAY_FILE)
    while True:
        time.sleep(1)

def initialize_threads():
    mapping_thread = threading.Thread(target=add_items_from_mappings, args=(LOCK,), daemon=True)
    latest_data_thread = threading.Thread(target=add_latest_data, args=(LOCK,),  daemon=True)
    historical_thread = threading.Thread(target=add_historical_data, args=(LOCK,), daemon=True)

    for t in [mapping_thread, latest_data_thread, historical_thread]:
        t.start()

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


if __name__ == "__main__":
    main()