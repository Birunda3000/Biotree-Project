import networkx as nx
import pandas as pd

def create_graph(nodes, edges, label):
    lab = {}
    G = nx.DiGraph()

    for i in range(len(nodes)):
        G.add_node(int(nodes[i]), label=label[i])
        lab[nodes[i]] = label[i]

    for i in range(len(edges)):
        G.add_edge(edges[i][0], edges[i][1])

    label_mapping = {node: data['label'] for node, data in G.nodes(data=True)}

    return G, lab, label_mapping

def load_graph(path_nodes, path_edges):
    df = pd.read_csv(path_nodes)

    dfr = pd.read_csv(path_edges)
    dfr = dfr.dropna().reset_index(drop=True)

    label = df["nome"].to_list()
    nodes = df["id"].to_list()

    ori = dfr["O-ID"].to_list()
    dest = dfr["D-ID"].to_list()

    edges = []
    for i in range(len(ori)):
        edges.append([ori[i], dest[i]])

    return create_graph(nodes, edges, label)

def return_components_in_topological_order(graph):
    components = list(nx.weakly_connected_components(graph))
    components_in_topological_order = []
    for component in components:
        subgraph = graph.subgraph(component)
        topological_order = list(nx.topological_sort(subgraph))
        components_in_topological_order.append(topological_order)
    return components_in_topological_order