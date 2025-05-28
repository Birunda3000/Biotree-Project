import os

import pandas as pd
from utils import load_graph, return_components_in_topological_order, Graph, evaluate_possible_solution

node_path = os.path.join(os.path.dirname(__file__), "bio-t.csv")
edge_path = os.path.join(os.path.dirname(__file__), "bio-relate.csv")

graph, labels, label_mapping = load_graph(node_path, edge_path)

order = return_components_in_topological_order(graph)

df = pd.read_csv(node_path, index_col="id")
df_edges = pd.read_csv(edge_path)
df_edges = df_edges.dropna().reset_index(drop=True)

grafo = Graph(label_mapping=label_mapping, components_in_topological_order=order, df_nodes=df, df_edges=df_edges)
grafo.print_info_table()
grafo.calculate_layout_quality()
grafo.draw()


res = grafo.get_current_solution()

res = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 0), (6, 4), (8, 5), (7, 2), (9, 0), (10, 1), (11, 2), (12, 6), (13, 8), (14, 7)]

print(res)

j = evaluate_possible_solution(res, grafo)
print(j)



#[(1, 0), (2, 1), (3, 2), (4, 3), (5, 0), (6, 4), (8, 5), (7, 2), (9, 0), (10, 1), (11, 2), (12, 6), (13, 8), (14, 7)]