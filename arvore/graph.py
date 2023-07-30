import itertools
import os

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from IPython.display import display
from utils import load_graph, return_components_in_topological_order, Graph

node_path = os.path.join(os.path.dirname(__file__), "bio-t.csv")
edge_path = os.path.join(os.path.dirname(__file__), "bio-relate.csv")

graph, labels, label_mapping = load_graph(node_path, edge_path)

# nx.draw(graph, labels=labels, with_labels=True)
# plt.show()
#nx.draw(graph, labels=label_mapping, with_labels=True)
plt.show()

order = return_components_in_topological_order(graph)
flattened_list = list(itertools.chain.from_iterable(order))
df = pd.read_csv(node_path, index_col="id")
df_edges = pd.read_csv(edge_path)
df_edges = df_edges.dropna().reset_index(drop=True)

i = 1
for subgraph in order:
    for node in subgraph:
        x1 = i
        y1 = -df.loc[node, "inicio"]

        x2 = i
        y2 = -df.loc[node, "fim"]

        plt.plot([x1, x2], [y1, y2], color="orange", linestyle="-", linewidth=6)
        plt.annotate(
            df.loc[node, "nome"],
            (x1, y1),
            color="black",
            fontsize=12,
            ha="center",
            va="center",
        )

        # take the lines that have the node as origin
        df_edges_origin = df_edges[df_edges["O-ID"] == node]
        for index, row in df_edges_origin.iterrows():
            x1 = i
            y1 = -df.loc[row["D-ID"], "inicio"]

            x2 = flattened_list.index(row["D-ID"]) + 1
            y2 = y1

            plt.arrow(
                x1,
                y1,
                x2 - x1,
                y2 - y1,
                color="black",
                linestyle="-",
                linewidth=1,
                head_width=0.1,
                head_length=0.1,
                length_includes_head=True,
            )
            plt.scatter(x1, y1, color="green", s=50)
            plt.scatter(x2, y2, color="black", s=100)

        i += 1
plt.show()

grafo = Graph(label_mapping=label_mapping, components_in_topological_order=order, df_nodes=df, df_edges=df_edges)
grafo.draw()
#grafo.print_info()


