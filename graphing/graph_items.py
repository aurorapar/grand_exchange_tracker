import math
import statistics

from scipy.signal import butter, lfilter, freqz

import matplotlib.pyplot as plt

from settings import *

def graph_items(
        title,
        item_names,
        x_label,
        y_label,
        items_to_graph
    ):

    graph_count = len(items_to_graph)
    row_count = math.sqrt(graph_count)
    if row_count != int(row_count):
        row_count += 1
    row_count = int(row_count)
    col_count = row_count
    while row_count > int(graph_count/row_count) + graph_count % row_count:
        row_count -= 1

    fig = plt.figure(layout="constrained")
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_edgecolor(FEATURE_COLOR)
    handles = []
    for items_index, item_data in enumerate(items_to_graph):
        axis = fig.add_subplot(row_count, col_count, items_index+1)
        item_name = item_names[items_index]
        fig.canvas.manager.set_window_title(item_name)

        x_values = item_data[0]
        x_labels = item_data[1]

        axis.set_title(f"{item_name}  Δt={DATESPLIT_TIME_DELTA}", color=FEATURE_COLOR)
        for ai, a in enumerate([axis, axis.twinx()]):
            y_values = [y[ai] for y in item_data[2]]
            y_labels = [y[ai] for y in item_data[3]]

            handle, = a.plot(x_values, y_values,
                      marker='.',
                      markersize=GRAPH_LINE_SIZE,
                      linestyle='solid',
                      linewidth=GRAPH_LINE_SIZE,
                      color=LINE_COLORS[ai],
                      label=y_label[ai]
            )
            handles.append(handle)

            if ai == 0:
                # prices axes
                date_ranges = draw_timedeltas(a.twinx(), x_values,max(y_values))

                # h, = plot_fourier_bullshit(a, MAGNITUDE_COLOR, x_values, y_values, date_ranges)
                h, = plot_moving_average(a, MOVING_AVG_COLOR, x_values, y_values, date_ranges)
                handles.append(h)

                annotate_values(a, LINE_COLORS[ai], x_values, y_values, date_ranges)
            else:
                # volumes axes
                # h, = plot_fourier_bullshit(a, MAGNITUDE_COLOR, x_values, y_values, date_ranges)
                # h, = plot_moving_average(a.twinx(), MOVING_AVG_COLOR, x_values, y_values, date_ranges)
                # handles.append(h)
                # annotate_values(a, LINE_COLORS[ai], x_values, y_values, date_ranges)
                pass

            a.locator_params(axis="y", nbins=5)
            plt.setp(a.get_yticklabels(), color=LINE_COLORS[ai])

            a.get_xaxis().set_visible(False)

            a.set_facecolor(BACKGROUND_COLOR)
            for spine in a.spines.values():
                spine.set_edgecolor(FEATURE_COLOR)



    legend = plt.legend(handles=handles,
                        shadow=True, fontsize='x-large',
                        labelcolor=FEATURE_COLOR,
                        facecolor=BACKGROUND_COLOR,
                        edgecolor=FEATURE_COLOR,
    )
    print("Sending...")
    plt.show()

def draw_timedeltas(axis, x_values, y_max, timedelta=DATESPLIT_TIME_DELTA):
    date_ranges = []
    start_date = x_values[0]
    current_date = start_date
    while current_date < x_values[-1]:
        next_date = current_date + timedelta
        date_ranges.append([current_date, next_date])
        day_string = current_date.strftime("%Y-%m-%d %H:%M")

        axis.vlines(current_date, 0, y_max, FEATURE_COLOR, linestyle="dotted")
        axis.annotate(day_string, xy=(current_date, 0), xycoords='data',
                   xytext=(.5, .5), textcoords='offset points', color=FEATURE_COLOR, rotation=90)
        current_date += timedelta
    return date_ranges


def annotate_values(axis, color, x_values, y_values, date_ranges):
    for date_range in date_ranges:
        min_date = date_range[0].replace(tzinfo=datetime.UTC)
        max_date = date_range[1].replace(tzinfo=datetime.UTC)
        values = [(x_values[yi], y) for yi, y in enumerate(y_values) if y and x_values[yi] and
              min_date <= x_values[yi].replace(tzinfo=datetime.UTC) < max_date ]
        if not values:
            continue
        values = sorted(values, key=lambda x: x[1])
        for point in [values[0], values[-1]]:
            point_string = f"{point[1]}  {point[0].strftime("@%H:%M")}"
            axis.annotate(point_string, xy=(point[0], point[1]), xycoords='data', rotation=50,
                       xytext=(1.5, 1.5), textcoords='offset points', color=color)
            axis.plot(point[0], point[1], 'o', color=color)

def plot_moving_average(axis, color, x_values, y_values, date_ranges, timedelta=MOVING_AVERAGE_TIME_DELTA):
    xs = []
    ys = []
    pairs = list(zip(x_values, y_values))
    pairs = [p for p in pairs if p[0] and p[1]]
    for t_index, timestamp in  enumerate(x_values):
        low_val = timestamp.replace(tzinfo=datetime.UTC) - timedelta
        if low_val < x_values[0].replace(tzinfo=datetime.UTC):
            continue

        sub_vals = sorted([p for p in pairs if low_val < p[0].replace(tzinfo=datetime.UTC) <= timestamp.replace(tzinfo=datetime.UTC)], key=lambda x: x[0].replace(tzinfo=datetime.UTC))
        xs.append(sub_vals[-1][0])
        ys.append(int(statistics.mean(x[1] for x in sub_vals)))
    annotate_values(axis, color, xs, ys, date_ranges)
    return axis.plot(xs, ys,
              marker='.',
              markersize=GRAPH_LINE_SIZE,
              linestyle='solid',
              linewidth=GRAPH_LINE_SIZE,
              color=color,
              label="Moving Price Avg"
              )

def plot_fourier_bullshit(axis, color, x_values, y_values, date_ranges):
    lowpass_y_values = list(map(int, butter_lowpass_filter(y_values, CUTOFF, SAMPLE_RATE, FOURIER_ORDER)))
    # pairs = list(zip(x_values, y_values, lowpass_y_values))
    # for p in pairs:
    #     output = [x for x in p]
    #     output.append(f"{p[1] / p[2] * 100:.0f}")
    #     print(output)
    annotate_values(axis.twinx(), color, x_values, lowpass_y_values, date_ranges)
    return axis.plot(x_values, lowpass_y_values,
         marker='.',
         markersize=GRAPH_LINE_SIZE,
         linestyle='solid',
         linewidth=GRAPH_LINE_SIZE,
         color=color,
         label="LPF (Price)"
    )

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, lfilter(b, a, data))
    return y




