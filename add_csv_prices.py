import csv
import os
import json

CSV_FILE = "prices.csv"
LAST_UPDATE = "%LAST_UPDATE%"
LAST_UPDATE2 = "%LAST_UPDATE_F%"
IGNORE_KEYS = [LAST_UPDATE, LAST_UPDATE2]

DATA_STORE_FILE = "prices.json"
DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), DATA_STORE_FILE)

def main():
    old_data = load_csv_data()
    current_data = load_cache()

    for item_name, item_data in old_data.items():
        if item_name in IGNORE_KEYS:
            pass

        if item_name not in current_data:
            current_data[item_name] = {}
        for time_stamp, item_price in item_data.items():
            current_data[item_name][time_stamp] = item_price

    with open(DATA_STORE_FILE, "w") as f:
        json.dump(current_data, f)

def load_csv_data():
    data = {}

    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        keys = reader.fieldnames
        for item_name in keys:
            if item_name not in data.keys():
                data[item_name] = {}
        for row in reader:
            updated_time = row[LAST_UPDATE]
            for item_name in keys:
                item_price = row[item_name]
                data[item_name][updated_time] = item_price

    return data

def load_cache():
    data = None

    with open(DATA_STORE_FILE, "r") as f:
        data = json.load(f)
        print("Cache loaded")
    return data

if __name__ == "__main__":
    main()