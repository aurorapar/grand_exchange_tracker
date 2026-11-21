import datetime

from database.item_operations import get_item

def get_old_history_items(timestamp):
    all_item_ids = get_item(expire_data=False)
    result = []
    for item in all_item_ids:
        if not item.history_processed:
            result.append(item)
            continue
        timestamp = timestamp.replace(tzinfo=datetime.UTC)
        item_timestamp = item.history_processed.replace(tzinfo=datetime.UTC)
        if timestamp > item_timestamp:
            result.append(item)
    return result
