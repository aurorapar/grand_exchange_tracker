import math

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

        axis.set_title(f"{item_name}", color=FEATURE_COLOR)
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

            highest = list(zip(x_values,y_values))
            highest = sorted(highest, key=lambda x: x[1])[-1]

            a.annotate(highest[1], xy=(highest[0], highest[1]), xycoords='data',
                          xytext=(1.5, 1.5), textcoords='offset points', color=LINE_COLORS[ai])
            a.plot(highest[0], highest[1], 'o', color=LINE_COLORS[ai])

            a.set_xlabel(x_label, color=FEATURE_COLOR)
            a.set_xticks(x_values, x_labels, color=FEATURE_COLOR)
            plt.setp(a.get_xticklabels(), rotation=30, horizontalalignment='right', color=FEATURE_COLOR)
            a.locator_params(axis="x", nbins=10)

            a.set_facecolor(BACKGROUND_COLOR)
            for spine in a.spines.values():
                spine.set_edgecolor(FEATURE_COLOR)

    plt.show()
