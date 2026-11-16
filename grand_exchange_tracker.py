import database.database
from api_calls.latest import get_latest_data
from api_calls.mapping import get_mapping_data
from api_calls.prices_volume_merge import get_prices_volume_merged
from database.item_operations import add_mapping_data, get_item_data
from database.itemdata_operations import add_latest_item_data, add_merged_data

from job.get_historical_data import get_historical_data

def main():
    database.database.initialize_database()
    # add_items()
    # add_latest_data()
    # add_price_volume()
    get_historical_data()

def add_items():
    # using a method so that memory can be garbage collected
    print("Getting Mapping data from api")
    mapping_data = get_mapping_data()
    print("Storing Mapping data in database")
    add_mapping_data(mapping_data)

def add_latest_data():
    print("Getting Items from database")
    items = get_item_data(expire_data=False)

    print("Getting Item data from api")
    item_total = len(items)
    item_count = 0

    while item_count < item_total:
        queried_items = items[:min(100, len(items))]
        add_latest_items_data(queried_items)
        item_count += 100
        print(f"\t{item_count/item_total*100:.0f}%", end="\r")
        items = items[min(100, len(items)):]


def add_latest_items_data(items):
    latest_items_data = get_latest_data(items)
    for latest_item_data in latest_items_data.values():
        add_latest_item_data(latest_item_data)


def add_price_volume():
    print("Getting Merged Price And Volume from api")
    merged_data = get_prices_volume_merged()
    print("Storing Merged Price And Volume in database")
    add_merged_data(merged_data)


if __name__ == "__main__":
    main()