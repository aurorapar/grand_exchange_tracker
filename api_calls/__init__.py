import json
import time

import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"}

def perform_request(url, sleep_time=0):
    response = requests.get(url, headers=headers)
    while response.status_code not in [200]:
        if "Too Many Requests" in response.reason:
            sleep_time += 1
            print(f"Sleeping for {sleep_time}s...")
            time.sleep(sleep_time)
            response = requests.get(url, headers=headers)
        else:
            raise RuntimeError(f"Couldn't get data: {response.status_code} {response.reason}")
    data = json.loads(response.text)
    sleep_time = max(sleep_time - 1, 0)
    return data