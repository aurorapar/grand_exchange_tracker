import datetime
import multiprocessing
import threading
import time

from graphing.highest_zscores import main as get_highest_zscores
from graphing.highest_volumes import main as get_highest_volumes
from graphing.graph_zscore_items import main as graph_zscore_items
from graphing.graph_volume_items import main as graph_volume_items

from settings import LOOKBACK_DAYS

LOCK = threading.Lock()

def main():
    lookback_date_cutoff = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=LOOKBACK_DAYS)

    # volumes = get_highest_volumes(lookback_date_cutoff)

    zscores = get_highest_zscores(lookback_date_cutoff)
    # input(zscores)
    # zscores = [(30066, 3.9659907955569667), (25454, 4.052224174983592), (23953, 4.154987422326744), (12484, 4.198585973713432), (9338, 4.341873031380608), (28313, 4.527244870157542), (30848, 7.211750536062137), (10145, 9.592217590206781)]

    display_multiple_graphs(lookback_date_cutoff, [z for z in zscores])

def display_multiple_graphs(lookback_date, graph_data):
    display_thread = threading.Thread(target=graph_via_process, args=(lookback_date, graph_data))
    display_thread.start()
    while True:
        time.sleep(1)

def graph_via_process(lookback_date, metrics):
    procs = []
    for metric in metrics:
        proc = multiprocessing.Process(target=graph_zscore_items, args=([metric], lookback_date))
        proc.start()
        procs.append(proc)
    for proc in procs:
        proc.join()

if __name__ == "__main__":
    main()