import itertools

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from enum import Enum, auto


def create_graph(nodes, edges, label):
    lab = {}
    G = nx.DiGraph()

    for i in range(len(nodes)):
        G.add_node(int(nodes[i]), label=label[i])
        lab[nodes[i]] = label[i]

    for i in range(len(edges)):
        G.add_edge(edges[i][0], edges[i][1])

    label_mapping = {node: data["label"] for node, data in G.nodes(data=True)}

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


class Node:
    def __init__(self, id, label, inicio, fim):
        self.id = id
        self.nome = label
        self.begin = inicio
        self.end = fim
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None

    def set_x1(self, x1):
        self.x1 = x1

    def set_x2(self, x2):
        self.x2 = x2

    def set_y1(self, y1):
        self.y1 = y1

    def set_y2(self, y2):
        self.y2 = y2


class Edge:
    def __init__(self, origin_id, destination_id):
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.origin_x = 0
        self.origin_y = 0
        self.destination_x = 0
        self.destination_y = 0

    def set_origin_x(self, origin_x):
        self.origin_x = origin_x

    def set_origin_y(self, origin_y):
        self.origin_y = origin_y

    def set_destination_x(self, destination_x):
        self.destination_x = destination_x

    def set_destination_y(self, destination_y):
        self.destination_y = destination_y

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

class Graph:
    def __init__(
        self, label_mapping, components_in_topological_order, df_nodes, df_edges
    ):
        self.label_mapping = label_mapping
        self.components_in_topological_order = components_in_topological_order
        self.nodes_list = {}
        self.edges_list = []
        self.df_edges = df_edges
        self.df_nodes = df_nodes
    
    def try_put_node(self, node_index, new_node, root, step):
        '''Try to put the node in the graph, if there is space, return True, else return False'''

        print(self.df_nodes.loc[node_index])

        if self.empty_space(x=root, y=-self.df_nodes.loc[node_index, "inicio"] and self.empty_space(x=root, y=-self.df_nodes.loc[node_index, "fim"])):
            new_node.set_x1(root)
            new_node.set_y1(-self.df_nodes.loc[node_index, "inicio"])

            new_node.set_x2(root)
            new_node.set_y2(-self.df_nodes.loc[node_index, "fim"])
            return True #put in the middle
        
        if self.empty_space(x=root+step, y=-self.df_nodes.loc[node_index, "inicio"]) and self.empty_space(x=root+step, y=-self.df_nodes.loc[node_index, "fim"]):
            new_node.set_x1(root)
            new_node.set_y1(-self.df_nodes.loc[node_index, "inicio"])

            new_node.set_x2(root)
            new_node.set_y2(-self.df_nodes.loc[node_index, "fim"])
            return True #put in the right
        
        if self.empty_space(x=root-step, y=-self.df_nodes.loc[node_index, "inicio"]) and self.empty_space(x=root-step, y=-self.df_nodes.loc[node_index, "fim"]):
            new_node.set_x1(root)
            new_node.set_y1(-self.df_nodes.loc[node_index, "inicio"])

            new_node.set_x2(root)
            new_node.set_y2(-self.df_nodes.loc[node_index, "fim"])
            return True #put in the left
        
        return False #no space

    def set_nodes_coordinates(self):
        '''Set the coordinates of the nodes in the graph'''
        root = 0
        for subgraph in self.components_in_topological_order:
            for node in subgraph:
                step = 0
                new_node = Node(
                    id=node,
                    label=self.df_nodes.loc[node, "nome"],
                    inicio=self.df_nodes.loc[node, "inicio"],
                    fim=self.df_nodes.loc[node, "fim"],
                )
                while not self.try_put_node(node_index=node, new_node=new_node, root=root, step=step):
                    step += 1
                self.nodes_list[node] = new_node

    def set_edges_coordinates(self):
        '''Set the coordinates of the edges in the graph'''
        for index, row in self.df_edges.iterrows():
            new_edge = Edge(origin_id=row["O-ID"], destination_id=row["D-ID"])

            y1 = self.nodes_list[row["D-ID"]].y1

            new_edge.set_origin_x(self.nodes_list[row["O-ID"]].x1)
            new_edge.set_origin_y(y1)

            new_edge.set_destination_x(self.nodes_list[row["D-ID"]].x1)
            new_edge.set_destination_y(y1)
            self.edges_list.append(new_edge)

    def draw(self):
        '''Draw the graph'''
        self.set_nodes_coordinates()
        self.set_edges_coordinates()

        for node in self.nodes_list.values():
            plt.plot(
                [node.x1, node.x2],
                [node.y1, node.y2],
                color="orange",
                linestyle="-",
                linewidth=6,
            )
            plt.annotate(
                node.nome,
                (node.x1, node.y1),
                color="black",
                fontsize=12,
                ha="center",
                va="center",
            )

        for edge in self.edges_list:
            plt.arrow(
                edge.origin_x,
                edge.origin_y,
                edge.destination_x - edge.origin_x,
                edge.destination_y - edge.origin_y,
                color="black",
                length_includes_head=True,
                head_width=0.1,
                head_length=0.1,
                width=0.001,
            )

        plt.show()

    def print_info(self):
        '''Print the nodes and edges of the graph'''
        print("Nodes:")
        for node in self.nodes_list.values():
            print(node.id, node.label, node.begin, node.end)
        print("Edges:")
        for edge in self.edges_list:
            print(edge.origin_id, edge.destination_id)
        
    def empty_space(self, x, y):
        '''Verify if there is an node occupying the space'''
        for node in self.nodes_list.values():
            if not node.x1 == node.x2:
                raise Exception("Node is not vertical")
            
            if node.x1 == x and node.x2 == x:
                if node.y1 <= y <= node.y2 or node.y2 <= y <= node.y1:
                    return False
        return True
