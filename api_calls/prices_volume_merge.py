from api_calls.volume import get_volume
from api_calls.price import get_prices

from constants import PRICE, VOLUME, IGNORE_KEYS, LAST_UPDATE

def get_prices_volume_merged():
    volume = get_volume()
    prices = get_prices()
    merger = {}

    for data_set in [volume, prices]:
        timestamp = data_set[LAST_UPDATE]
        key = VOLUME if data_set == volume else PRICE

        for item_name, value in data_set.items():
            if item_name in IGNORE_KEYS:
                continue

            if item_name not in merger:
                merger[item_name] = {}
            if timestamp not in merger[item_name]:
                merger[item_name][timestamp] = {}
            merger[item_name][timestamp][key] = value

    return merger
