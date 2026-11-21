from api_calls import perform_request


def main():
    endpoint = "https://prices.runescape.wiki/api/v2/osrs/5m"
    return perform_request(endpoint)