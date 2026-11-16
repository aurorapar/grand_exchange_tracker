import datetime
import json
import os
import shutil

from constants import BACKUP_DATA_STORE_FILE

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def load_data(file_path):
    data = None
    if not os.path.exists(file_path):
        print("Creating new cache, doesn't exist")
        data = {}
        save_data(file_path, data)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            print("Cache loaded")
    except Exception as e:
        print("Error loading cache:", e)
        backup_data(file_path)
        print("Creating new cache")
        data = {}
        save_data(file_path, data)

    return data

def backup_data(data_file):
    print("Backing up cache...")
    now = datetime.datetime.now()
    now = datetime.datetime.strftime(now, "%Y%m%d%H%M%S")
    file_name, file_extension = os.path.splitext(data_file)
    backup_file_name = BACKUP_DATA_STORE_FILE.format(now, file_extension)
    with open(backup_file_name, "w") as f:
        shutil.copy(data_file, backup_file_name)
    print("Cache Updated")