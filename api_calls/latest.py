from api_calls import perform_request

def get_latest_data(items):
    item_ids = f"|".join([str(item.id) for item in items])
    endpoint = "https://api.weirdgloop.org/exchange/history/osrs/latest?id={0}".format(item_ids)
    return perform_request(endpoint)