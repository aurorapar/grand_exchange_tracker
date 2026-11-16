import concurrent.futures
import traceback

from api_calls.historical_price_volume import get_historical_price_volume
from database.item_operations import get_item_data
from database.itemdata_operations import add_item_history
from constants import TIMESTAMP
from settings import THREAD_COUNT

def get_historical_data():
    all_item_ids = get_all_item_ids()
    item_count = len(all_item_ids)
    for x in range(100, item_count, 100):
        print(x-100, x)
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            [executor.submit(update_item_id_history, item_id) for item_id in all_item_ids[x-100:x]]

def get_all_item_ids():
    all_item_ids = get_item_data(expire_data=False)
    return [item.id for item in all_item_ids]

def update_item_id_history(item_id):
    item_history = get_historical_price_volume(item_id)
    if str(item_id) in item_history:
        data = item_history[str(item_id)]
        data_length = len(data)
        for data_index, data_piece in enumerate(data):
            try:
                item_data = data_piece
                item_data[TIMESTAMP] = item_data[TIMESTAMP] / 1000
                add_item_history(data_piece)

            except Exception as exc:
                print(f'{item_id} generated an exception')
                print(data_piece)
                traceback.print_exc()
                input("Paused")

            # print(f"Item {data_index/data_length*100:.0f}%", end="\r")
            # print(f"Total {future_index / item_count*100:.0f}%", end="\r")

