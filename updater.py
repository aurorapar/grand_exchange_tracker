import threading
import time

from database.database import initialize_database
from job.get_latest_data import main as get_latest_data
from job.get_historical_data import get_historical_data

LOCK = threading.Lock()

def main():
    initialize_database()

    jobs = [
        threading.Thread(target=five_minute_tracker_job, daemon=True)
        ,threading.Thread(target=historical_tracker_job, daemon=True)
    ]
    for job in jobs:
        job.start()

    print("Jobs started")
    while True:
        time.sleep(1)

def five_minute_tracker_job():
    while True:
        get_latest_data(LOCK)
        time.sleep(300)

def historical_tracker_job():
    while True:
        get_historical_data(LOCK)
        time.sleep(60 * 60 * 6)

if __name__ == '__main__':
    main()