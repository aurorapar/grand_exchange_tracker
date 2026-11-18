import multiprocessing

from constants import *

PROCESSES_TO_SPAWN = multiprocessing.cpu_count()
THREAD_COUNT = 10

TRACKED_ITEMS = ["Black set (lg)", "Black salamander"]

NUMBER_OF_ZSCORES = 7

BACKGROUND_COLOR = BLACK
LINE_COLOR = BLUE
FEATURE_COLOR = PINK
GRAPH_LINE_SIZE = 1.0

MAX_GRAPH_LABELS = 10

# dont graph if threshold function is true
THRESHOLDS = [
    lambda price, volume:  (price < 10000 and volume < 10000)
]
THRESHOLD_SAMPLE_POINTS = 100
