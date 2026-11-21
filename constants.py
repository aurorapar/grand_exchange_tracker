import os
import multiprocessing

PRICE_DATA_STORE_FILE = "json_data/prices.json"
PRICE_DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), PRICE_DATA_STORE_FILE)

ALL_PRICE_DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), "json_data/all_prices.json")

VOLUME_DATA_STORE_FILE = "json_data/volume.json"
VOLUME_DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), VOLUME_DATA_STORE_FILE)

MAPPING_DATA_STORE_FILE = "json_data/mappings.json"
MAPPING_DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), MAPPING_DATA_STORE_FILE)

BACKUP_DATA_STORE_FILE = f"json_data/data_backup_{0}.{1}"
BACKUP_DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), BACKUP_DATA_STORE_FILE)

DATABASE_FILE = "database/database.sqlite"
DATABASE_FILE = os.path.join(os.path.dirname(__file__), DATABASE_FILE)

DISPLAY_FILE = os.path.join(os.path.dirname(__file__), "display.py")

PRICES = "prices"
LAST_UPDATE = "%LAST_UPDATE%"
LAST_UPDATE2 = "%LAST_UPDATE_F%"
IGNORE_KEYS = [LAST_UPDATE, LAST_UPDATE2]

PINK = (1,0,150/255)
BLACK = (0,0,0)
BLUE = 'tab:blue'
YELLOW = (1,1,0)

DATA = "data"
ITEM_NAME = "name"
ZSCORE = "zscore"
ZSCORES = "zscores"
ZSCORE_DEV = "zscore_deviation"
TIMESTAMP = "timestamp"
ITEM_ID = "id"
AVG_HIGH = "avgHighPrice"
AVG_LOW = "avgLowPrice"
HIGH_PRICE_VOLUME = "highPriceVolume"
LOW_PRICE_VOLUME = "lowPriceVolume"
DAILY_AVG = "dailyAvg"
PRICE = "price"
VOLUME = "volume"
RUNESCAPE_ITEM_ID = "runescape_item_id"
PRICE_MAX = "price_max"
PRICE_MIN = "price_min"
VOLUME_MAX = "volume_max"
VOLUME_MIN = "volume_min"