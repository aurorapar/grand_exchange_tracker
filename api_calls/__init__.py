import json

import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"}

def perform_request(url):
    response = requests.get(url, headers=headers)
    if response.status_code not in [200]:
        raise RuntimeError(f"Couldn't get data: {response.status_code} {response.reason}")
    data = json.loads(response.text)
    return data