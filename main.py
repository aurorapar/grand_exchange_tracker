import json
import csv
import os
import shutil
import time
import datetime
import multiprocessing

import requests

LAST_UPDATE = "%LAST_UPDATE%"
LAST_UPDATE2 = "%LAST_UPDATE_F%"
IGNORE_KEYS = [LAST_UPDATE, LAST_UPDATE2]
DATA_STORE_FILE = "prices.json"
DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), DATA_STORE_FILE)
PRICES = "prices"
PROCESSES_TO_SPAWN = multiprocessing.cpu_count()
LOCK = multiprocessing.Lock()

def main():
    while True:
        print("Performing main loop")
        new_data = get_api_data()
        update_cache(new_data)
        backup_data()
        # time.sleep(60 * 60)  # 1 hour
        time.sleep(10)

def get_api_data():
    print("Getting API data")
    api_endpoint = "https://oldschool.runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"  # API calls for prices and item names
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"}

    grand_exchange_data_request = requests.get(url=api_endpoint, headers=headers)
    if grand_exchange_data_request.status_code not in [200]:
        code = grand_exchange_data_request.status_code
        reason = grand_exchange_data_request.text
        raise RuntimeError(f"Couldn't get data: {code} {reason}")
    ge_data = json.loads(grand_exchange_data_request.text)
    return ge_data

def update_cache(new_data):
    print("Updating cache")
    update_time = new_data[LAST_UPDATE]
    print(f"{len(new_data) - len(IGNORE_KEYS)} items to update")
    data = load_cache()
    for item_name, item_price in new_data.items():

        if item_name in IGNORE_KEYS:
            pass

        if item_name not in data:
            data[item_name] = {

            }
        data[item_name][update_time] = item_price

    save_data(data)

def save_data(data):
    with open(DATA_STORE_FILE, "w") as f:
        json.dump(data, f)

def load_cache():
    data = None
    if not os.path.exists(DATA_STORE_FILE):
        print("Creating new cache, doesn't exist")
        data = {}
        save_data(data)
    try:
        with open(DATA_STORE_FILE, "r") as f:
            data = json.load(f)
            print("Cache loaded")
    except Exception as e:
        print("Error loading cache:", e)
        backup_data()
        print("Creating new cache")
        data = {}
        save_data()

    return data

def backup_data():
    with LOCK:
        print("Backing up cache...")
        now = datetime.datetime.now()
        now = datetime.datetime.strftime(now, "%Y%m%d%H%M%S")
        backup_file_name = os.path.join(os.path.dirname(__file__), f"data_backup_{now}.json")
        with open(backup_file_name, "w") as f:
            shutil.copy(DATA_STORE_FILE, backup_file_name)
        print("Cache Updated")



if __name__ == "__main__":
    main()