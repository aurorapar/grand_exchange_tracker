from api_calls import perform_request


def get_mapping_data():
    endpoint = "https://prices.runescape.wiki/api/v2/osrs/mapping"
    return perform_request(endpoint)