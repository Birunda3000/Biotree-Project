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
#plt.show()

order = return_components_in_topological_order(graph)
flattened_list = list(itertools.chain.from_iterable(order))
df = pd.read_csv(node_path, index_col="id")
df_edges = pd.read_csv(edge_path)
df_edges = df_edges.dropna().reset_index(drop=True)


grafo = Graph(label_mapping=label_mapping, components_in_topological_order=order, df_nodes=df, df_edges=df_edges)
grafo.draw()
