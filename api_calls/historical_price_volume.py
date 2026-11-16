from api_calls import perform_request


def get_historical_price_volume(item_id):
    endpoint = "https://api.weirdgloop.org/exchange/history/osrs/all"
    item_id = f"?id={item_id}"
    return perform_request(endpoint + item_id)
