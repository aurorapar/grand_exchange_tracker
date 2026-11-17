import json
import time

import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"}
SLEEP_TIME = 0

def perform_request(url):
    global SLEEP_TIME
    response = requests.get(url, headers=headers)
    if response.status_code not in [200]:
        if "Too Many Requests" in response.reason:
            SLEEP_TIME += 1
            print(f"Sleeping for {SLEEP_TIME}s...")
            time.sleep(SLEEP_TIME)
            return perform_request(url)
        raise RuntimeError(f"Couldn't get data: {response.status_code} {response.reason}")
    data = json.loads(response.text)
    SLEEP_TIME = max(SLEEP_TIME - 1, 0)
    return data