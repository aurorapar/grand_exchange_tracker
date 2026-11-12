import matplotlib.pyplot as plt

from settings import *

def graph_items(
        title,
        item_names,
        x_label,
        y_label,
        items_to_graph
    ):

    fig, axs = plt.subplots(len(items_to_graph))
    fig.suptitle(title, color=FEATURE_COLOR)
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_edgecolor(FEATURE_COLOR)

    for items_index, item_data in enumerate(items_to_graph):
        item_name = item_names[items_index]

        x_values = item_data[0]
        x_labels = item_data[1]
        y_values = item_data[2]
        y_labels = item_data[3]

        axs[items_index].set_title(f"{item_name}", color=FEATURE_COLOR)
        axs[items_index].plot(x_values, y_values,
                 marker='.',
                 linestyle='solid',
                 color=LINE_COLOR
                 )

        axs[items_index].set_xlabel(x_label, color=FEATURE_COLOR)
        axs[items_index].set_ylabel(y_label, color=FEATURE_COLOR)

        axs[items_index].set_xticks(x_values, x_labels, color=FEATURE_COLOR)
        axs[items_index].set_yticks(y_values, y_labels, color=FEATURE_COLOR)

        axs[items_index].tick_params(which="both", labelsize="small", color=FEATURE_COLOR)

        plt.setp(axs[items_index].get_xticklabels(), rotation=30, horizontalalignment='right', color=FEATURE_COLOR)

        for score in list(zip(item_data[0], item_data[2])):
            axs[items_index].annotate(f"{score[1]:.2f}",
                        xy=(score[0], score[1]), xycoords='data',
                        xytext=(1.5, 1.5), textcoords='offset points', color=FEATURE_COLOR)

        axs[items_index].set_facecolor(BACKGROUND_COLOR)
        for spine in axs[items_index].spines.values():
            spine.set_edgecolor(FEATURE_COLOR)

    plt.tight_layout()
    plt.show()
