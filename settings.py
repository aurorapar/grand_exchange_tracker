import datetime

from constants import *

THREAD_COUNT = 10

# graph this number of items
NUMBER_OF_ITEMS_TO_GRAPH = 1

BACKGROUND_COLOR = BLACK
# first line color is price,
# second line color is volume
LINE_COLORS = [
    BLUE,
    YELLOW
]
MAGNITUDE_COLOR = ORANGE
MOVING_AVG_COLOR = ORANGE
FEATURE_COLOR = PINK
LEGEND_BACKGROUND = DARK_GRAY
GRAPH_LINE_SIZE = 2.0

# skip item if threshold function is true
# uses average price and volume over a time span
# MUST ALWAYS use price and volume as input,
# additional filters would need different code/logic
THRESHOLDS = [
    lambda price, volume:  (price < 10000 or volume < 10000),
    # lambda price, volume:  (price < 10000 or volume < 10000),
]

# Skip updating items if API data is younger than this value
API_REFRESH = datetime.timedelta(hours=12)

# number of days to consider for all data
# current_date - LOOKBACK_DAYS
LOOKBACK_DAYS = 30

# splits vertical time lines of x-axis
DATESPLIT_TIME_DELTA = datetime.timedelta(days=1)

# fourier bullshit
FOURIER_ORDER = 10
SAMPLE_RATE = 60000
CUTOFF = 10000

# Moving Average Size
MOVING_AVERAGE_TIME_DELTA = datetime.timedelta(days=1)