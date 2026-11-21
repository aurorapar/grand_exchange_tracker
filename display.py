import datetime
import multiprocessing
import threading
import time

from graphing.highest_zscores import main as get_highest_zscores
from graphing.highest_volumes import main as get_highest_volumes
from graphing.graph_zscore_items import main as graph_zscore_items
from graphing.graph_volume_items import main as graph_volume_items

from settings import LOOKBACK_DAYS

user_options = {
    "Graph Highest Volumes": get_highest_volumes,
    "Graph Highest Z-Scores": get_highest_zscores,
}
def show_user_options():
    # volumes = get_highest_volumes(lookback_date_cutoff)
    # zscores = get_highest_zscores(lookback_date_cutoff)
    # display_multiple_graphs(lookback_date_cutoff, zscores)

    while True:
        lookback_date_cutoff = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=LOOKBACK_DAYS)
        input("Test")
        # for display_option, callback in user_options.items():
        #   pass

def display_multiple_graphs(lookback_date, zscores):
    display_thread = threading.Thread(target=graph_via_process, args=(lookback_date, zscores))
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
