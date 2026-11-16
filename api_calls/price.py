from api_calls import perform_request

def get_prices():
    endpoint = "https://oldschool.runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"
    return perform_request(endpoint)