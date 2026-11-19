import datetime

from constants import *

THREAD_COUNT = 10

# graph this number of items
NUMBER_OF_ITEMS_TO_GRAPH = 8

BACKGROUND_COLOR = BLACK
LINE_COLORS = [
    BLUE,
    YELLOW
]
FEATURE_COLOR = PINK
GRAPH_LINE_SIZE = 1.0

# skip item if threshold function is true
# uses average price and volume over a time span
THRESHOLDS = [
    lambda price, volume:  (price < 10000 and volume < 10000)
]

# number of most recent points for average volume calculations
# increase to use older data when determining average volume for threshold
THRESHOLD_SAMPLE_POINTS = 100

# Skip updating items if API data is younger than this value
API_REFRESH = datetime.timedelta(hours=12)

# number of days to consider for all data
# current_date - LOOKBACK_DAYS
LOOKBACK_DAYS = 900