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
    print(row_count, col_count)

    fig = plt.figure(layout="constrained")
    fig.suptitle(title, color=FEATURE_COLOR)
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_edgecolor(FEATURE_COLOR)
    # fig.tight_layout()

    print("")
    for items_index, item_data in enumerate(items_to_graph):
        axis = fig.add_subplot(row_count, col_count, items_index+1)

        item_name = item_names[items_index]

        x_values = item_data[0]
        x_labels = item_data[1]
        y_values = item_data[2]
        y_labels = item_data[3]

        axis.set_title(f"{item_name}", color=FEATURE_COLOR)
        axis.plot(x_values, y_values,
            marker='.',
            markersize=GRAPH_LINE_SIZE,
            linestyle='solid',
            linewidth=GRAPH_LINE_SIZE,
            color=LINE_COLOR
                 )

        axis.set_xlabel(x_label, color=FEATURE_COLOR)
        axis.set_ylabel(y_label, color=FEATURE_COLOR)

        axis.set_xticks(x_values, x_labels, color=FEATURE_COLOR)
        # axis.set_yticks(y_values, color=FEATURE_COLOR)

        axis.locator_params(axis="x", nbins=10)
        axis.locator_params(axis="y", nbins=10)

        axis.tick_params(which="both", labelsize="small", color=FEATURE_COLOR)

        plt.setp(axis.get_xticklabels(), rotation=30, horizontalalignment='right', color=FEATURE_COLOR)
        plt.setp(axis.get_yticklabels(), color=FEATURE_COLOR)

        max_y_point = list(zip(item_data[0], item_data[2]))
        max_y_point = sorted(max_y_point, key=lambda x: x[1])[-1]

        axis.annotate(f"{max_y_point[1]:.0f}",
                        xy=(max_y_point[0], max_y_point[1]), xycoords='data',
                        xytext=(1.5, 1.5), textcoords='offset points', color=FEATURE_COLOR)
        axis.plot(max_y_point[0], max_y_point[1], 'o')

        axis.set_facecolor(BACKGROUND_COLOR)
        for spine in axis.spines.values():
            spine.set_edgecolor(FEATURE_COLOR)

    plt.show()
