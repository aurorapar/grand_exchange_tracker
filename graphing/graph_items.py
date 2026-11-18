import math

import matplotlib.pyplot as plt
import numpy

from settings import *

def graph_items(
        title,
        item_names,
        x_label,
        y_label,
        items_to_graph
    ):

    fig, main_axis = plt.subplots(len(items_to_graph), sharex=True)
    fig.set_layout_engine(constrained_layout=True)
    # fig.tight_layout()
    fig.suptitle(title, color=FEATURE_COLOR)
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_edgecolor(FEATURE_COLOR)

    graph_count = len(items_to_graph)

    row_col_count = math.sqrt(graph_count)
    if row_col_count != int(row_col_count):
        row_col_count = int(row_col_count) + 1
    row_col_count = int(row_col_count)

    subfigures = fig.subfigures(nrows=row_col_count, ncols=row_col_count,
                                facecolor=BACKGROUND_COLOR, hspace=.2)
    sub_axes = []

    for subfigure in fig.subfigs:
            setup_subfigures(subfigure, sub_axes)
    for a in sub_axes:
        a.set_facecolor(BACKGROUND_COLOR)

    print("")
    for items_index, item_data in enumerate(items_to_graph):
        axs = sub_axes[items_index]

        item_name = item_names[items_index]

        x_values = item_data[0]
        x_labels = item_data[1]
        y_values = item_data[2]
        y_labels = item_data[3]

        axs.set_title(f"{item_name}", color=FEATURE_COLOR)
        axs.plot(x_values, y_values,
            marker='.',
            markersize=GRAPH_LINE_SIZE,
            linestyle='solid',
            linewidth=GRAPH_LINE_SIZE,
            color=LINE_COLOR
                 )

        axs.set_xlabel(x_label, color=FEATURE_COLOR)
        axs.set_ylabel(y_label, color=FEATURE_COLOR)

        axs.set_xticks(x_values, x_labels, color=FEATURE_COLOR)
        # axs.set_yticks(y_values, color=FEATURE_COLOR)

        axs.locator_params(axis="x", nbins=10)
        axs.locator_params(axis="y", nbins=10)

        axs.tick_params(which="both", labelsize="small", color=FEATURE_COLOR)

        plt.setp(axs.get_xticklabels(), rotation=30, horizontalalignment='right', color=FEATURE_COLOR)
        plt.setp(axs.get_yticklabels(), color=FEATURE_COLOR)

        max_y_point = list(zip(item_data[0], item_data[2]))
        max_y_point = sorted(max_y_point, key=lambda x: x[1])[-1]

        axs.annotate(f"{max_y_point[1]:.0f}",
                        xy=(max_y_point[0], max_y_point[1]), xycoords='data',
                        xytext=(1.5, 1.5), textcoords='offset points', color=FEATURE_COLOR)

        for spine in axs.spines.values():
            spine.set_edgecolor(FEATURE_COLOR)

    plt.show()

def setup_subfigures(subfigure, sub_axes):
    subfigure.set_facecolor(BACKGROUND_COLOR)
    parent_axes = subfigure.subplots(nrows=1, ncols=1)
    sub_axes += [parent_axes]

