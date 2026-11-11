import os
import multiprocessing

DATA_STORE_FILE = "prices.json"
DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), DATA_STORE_FILE)

PRICES = "prices"
LAST_UPDATE = "%LAST_UPDATE%"
LAST_UPDATE2 = "%LAST_UPDATE_F%"
IGNORE_KEYS = [LAST_UPDATE, LAST_UPDATE2]

PINK = (1,0,150/255)
BLACK = (0,0,0)
BLUE = 'tab:blue'