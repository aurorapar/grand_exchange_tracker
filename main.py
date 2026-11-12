import json
import shutil
import datetime
import statistics

import requests

from settings import *

LOCK = multiprocessing.Lock()

def main():
    print("Performing main loop")
    new_data = get_api_data()
    update_cache(new_data)
    backup_data()

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
    print(f"TImestamp: {ge_data[LAST_UPDATE]} {ge_data[LAST_UPDATE2]}")
    return ge_data

def update_cache(new_data):
    print("Updating cache")
    print(f"{len(new_data) - len(IGNORE_KEYS)} items in cache")
    data = load_cache()

    clears = list()
    for k, v in data.items():
        for v1,v2 in v.items():
            if not isinstance(v1, int) or not isinstance(v2, int):
                clears.append((k, v1))
    for c in clears:
        item_name = c[0]
        time_stamp = c[1]
        try:
            data[item_name][int(time_stamp)] = int(data[item_name][time_stamp])
        except Exception as e:
            print(e)
            data[item_name][int(time_stamp)] = int(data[item_name][int(time_stamp)])
        try:
            del data[item_name][time_stamp]
        except:
            pass

    for k,v in new_data.items():
        if k in IGNORE_KEYS:
            continue
        if k not in data:
            data[k] = {}
        data[k][int(new_data[LAST_UPDATE])] = int(v)

    # with multiprocessing.Manager() as mgr:
    #     pool_data = mgr.dict(data)
    #     for k, v in pool_data.items():
    #         pool_data[k] = mgr.dict(v)
    #     pool_counter = mgr.Value('i', 0)
    #     with multiprocessing.Pool(PROCESSES_TO_SPAWN) as pool:
    #         pool.map(
    #             update_data,
    #             ((item_name, price, new_data[LAST_UPDATE], pool_data, pool_counter) for item_name, price in new_data.items())
    #         )
    #     print("")
    #     print("Done")
    #     data = dict(pool_data)
    #     for k,v in data.items():
    #         data[k] = dict(v)
    save_data(data)

def update_data(new_data):
    item_name = new_data[0]
    if item_name in IGNORE_KEYS:
        return
    price = new_data[1]
    update_time = new_data[2]
    old_data = new_data[3]
    counter = new_data[4]
    if item_name not in old_data:
        old_data[item_name] = {}
    old_data[item_name][update_time] = price
    # print(f"Updated {k} to {v}")
    counter.value += 1
    print(f"Items Updated: {counter.value}", end='\r')

def save_data(data):
    with open(DATA_STORE_FILE, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def load_cache():
    with LOCK:
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
            save_data(data)

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

def calculate_scores(data):
    scores = []
    for item_name, item_data in data.items():

        if item_name in IGNORE_KEYS:
            continue
        zscore = {
            ITEM_NAME: item_name,
            TIMESTAMP: [],
            ZSCORES: [],
            ZSCORE_DEV: None
        }
        item_scores = [(int(t), int(s)) for t, s in item_data.items()]
        item_scores = sorted(item_scores, key=lambda x: x[0])

        for index in range(len(item_scores) + 1):
            if index < 2:
                continue
            sub_prices = [x[1] for x in item_scores][:index]
            time_stamp = [x[0] for x in item_scores][:index][-1]
            price = sub_prices[-1]
            s = statistics.stdev(sub_prices)
            if s == 0:
                zscore[ZSCORES].append(s)
            else:
                m = statistics.mean(sub_prices)
                zscore[ZSCORES].append((price - m) / s)
            zscore[TIMESTAMP].append(time_stamp)

            if not zscore[ZSCORES]:
                print(f"Not enough data to graph item {item_name}")
                exit()

            try:
                zscore[ZSCORE_DEV] = statistics.stdev(zscore[ZSCORES])
            except Exception as e:
                print(f"Error trying to calculate z-score stddev data for {item_name}, skipping\n\t{zscore[ZSCORES]}")
                print(f"\tValues: {zscore[TIMESTAMP]} {zscore[ZSCORES]}")

        scores.append(zscore)

    return scores

if __name__ == "__main__":
    main()