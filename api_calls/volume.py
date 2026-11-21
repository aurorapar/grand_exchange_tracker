from api_calls import perform_request

def get_volume():
    endpoint = "https://oldschool.runescape.wiki/?title=Module:GEVolumes/data.json&action=raw&ctype=application%2Fjson"
    return perform_request(endpoint,0)