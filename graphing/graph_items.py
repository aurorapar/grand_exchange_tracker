import math
import statistics

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
            a.plot(x_values, y_values,
                      marker='.',
                      markersize=GRAPH_LINE_SIZE,
                      linestyle='solid',
                      linewidth=GRAPH_LINE_SIZE,
                      color=LINE_COLORS[ai]
                      )
            a.set_ylabel(y_label[ai], color=LINE_COLORS[ai])
            a.locator_params(axis="y", nbins=5)
            plt.setp(a.get_yticklabels(), color=LINE_COLORS[ai])


            highest = [(x, y_values[xi]) for xi, x in enumerate(x_values) if x and y_values[xi]]
            highest = sorted(highest, key=lambda x: x[1])[-1]

            a.set_xlabel(x_label, color=FEATURE_COLOR)
            a.get_xaxis().set_visible(False)
            # a.set_xticks(x_values, x_labels, color=FEATURE_COLOR)
            # plt.setp(a.get_xticklabels(), rotation=30, horizontalalignment='right', color=FEATURE_COLOR)
            # a.locator_params(axis="x", nbins=10)

            a.set_facecolor(BACKGROUND_COLOR)
            for spine in a.spines.values():
                spine.set_edgecolor(FEATURE_COLOR)

            start_date = x_values[0]
            line_values = [(x_values[yi], y) for yi, y in enumerate(y_values) if y and x_values[yi]]
            y_min = min(x[1] for x in line_values)
            y_max = max(x[1] for x in line_values)
            current_date = line_values[0][0]
            while current_date < line_values[-1][0]:
                next_date = current_date + DATESPLIT_TIME_DELTA

                day_string = current_date.strftime("%Y-%m-%d %H:%M")
                if ai == 0:
                    a.vlines(current_date, y_min, y_max, FEATURE_COLOR, linestyle="dotted")
                    a.annotate(day_string, xy=(current_date, y_min), xycoords='data',
                               xytext=(.5, .5), textcoords='offset points', color=FEATURE_COLOR, rotation=90)

                day_y_values = [y for yi, y in enumerate(line_values) if current_date <= y[0] < next_date]
                if not day_y_values:
                    current_date = next_date
                    continue
                day_y_values = sorted(day_y_values, key=lambda x: x[1])
                min_point = day_y_values[0]
                max_point = day_y_values[-1]
                for point in [min_point, max_point]:
                    point_string = f"{point[1]}  {point[0].strftime("@%H:%M")}"
                    a.annotate(point_string, xy=(point[0], point[1]), xycoords='data', rotation=50,
                               xytext=(1.5, 1.5), textcoords='offset points', color=LINE_COLORS[ai])
                    a.plot(point[0], point[1], 'o', color=LINE_COLORS[ai])
                current_date = next_date

    plt.show()
