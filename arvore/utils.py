import itertools
from enum import Enum, auto

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from IPython.display import display


def create_graph(nodes: list, edges: list, label: list) -> tuple:
    """Create a graph from the nodes and edges lists and return a tuple with the graph, the labels and the label mapping"""
    lab = {}
    G = nx.DiGraph()

    for i in range(len(nodes)):
        G.add_node(int(nodes[i]), label=label[i])
        lab[nodes[i]] = label[i]

    for i in range(len(edges)):
        G.add_edge(edges[i][0], edges[i][1])

    label_mapping = {node: data["label"] for node, data in G.nodes(data=True)}

    return G, lab, label_mapping


def load_graph(path_nodes: str, path_edges: str) -> tuple:
    """Load the graph from the csv files and return a tuple with the graph, the labels and the label mapping"""
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
    def __init__(self, id: int, label: str, origin: int, extinction: int):
        self.id = id
        self.nome = label
        self.origin = origin
        self.extinction = extinction
        self.x = None

    def set_x(self, x):
        self.x = x

    def __str__(self) -> str:
        return f"Node {self.id} - {self.nome} - {self.origin} - {self.extinction}"


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
    
    def __str__(self) -> str:
        #return f"Edge {self.origin_id} - {self.destination_id}"
        return f"Edge {self.origin_id} - {self.destination_id} - {self.origin_x} - {self.origin_y} - {self.destination_x} - {self.destination_y}"

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

        # fill the nodes_list with the info in the df_nodes

        flattened_list = [item for sublist in components_in_topological_order for item in sublist]

        for index, row in self.df_nodes.iterrows():
            self.nodes_list[int(index)] = Node(
                id=int(index),
                label=row["nome"],
                origin=int(-row["inicio"]),
                extinction=int(-row["fim"]),
            )
            self.nodes_list[index].set_x(flattened_list.index(index))
            #self.nodes_list[index].set_x(index)

        # fill the edges_list with the info in the df_edges
        for index, row in self.df_edges.iterrows():
            self.edges_list.append(
                Edge(origin_id=row["O-ID"], destination_id=row["D-ID"])
            )
    
    def set_edges_coordinates(self):
        """Set the coordinates of the edges in the graph"""
        for edge in self.edges_list:

            y = self.nodes_list[edge.destination_id].origin

            edge.origin_x = self.nodes_list[edge.origin_id].x
            edge.origin_y = y

            edge.destination_x = self.nodes_list[edge.destination_id].x
            edge.destination_y = y

    
    def draw(self):
        """Draw the graph"""
        #self.set_nodes_coordinates()
        self.set_edges_coordinates()

        print(self.components_in_topological_order)

        for node in self.nodes_list.values():
            plt.plot(
                [node.x, node.x],
                [node.origin, node.extinction],
                color="orange",
                linestyle="-",
                linewidth=6,
            )
            plt.annotate(
                node.nome,
                (node.x, node.origin),
                color="black",
                fontsize=12,
                ha="center",
                va="center",
            )
        
        for edge in self.edges_list:
            print(edge)
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

    def set_nodes_coordinates(self):
        """Set the coordinates of the nodes in the graph"""
        pass

    def verify_space(self, x, y_o, y_e):
        """Verify if there is an node can be put in the space"""
        for node in self.nodes_list.values():
            if node.x != x:
                pass
                #continue
            elif y_e < node.origin:
                continue
            elif y_o > node.extinction:
                continue
            else:
                return False
        return True

    def test_verify_space(self):
        x1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        x2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_o = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_e = [0, 0, 0, 0, 0, 0, 0, 0, 0]


'''
    def try_put_node(self, node_index, new_node, root, step):
        """Try to put the node in the graph, if there is space, return True, else return False"""

        # if self.empty_space(x=root, y=-self.df_nodes.loc[node_index, "inicio"] and self.empty_space(x=root, y=-self.df_nodes.loc[node_index, "fim"])):

        if self.empty_space(
            x1=root,
            y1=-self.df_nodes.loc[node_index, "inicio"],
            x2=root,
            y2=-self.df_nodes.loc[node_index, "fim"],
        ):
            new_node.set_x1(root)
            new_node.set_y1(-self.df_nodes.loc[node_index, "inicio"])

            new_node.set_x2(root)
            new_node.set_y2(-self.df_nodes.loc[node_index, "fim"])
            print("--------------------------------------------------")
            print("Node: ", new_node)
            print("X: ", root)
            print("Root: ", root)
            print("Step: ", step)
            print("--------------------------------------------------")
            return True  # put in the middle

        # if self.empty_space(x=root + step, y=-self.df_nodes.loc[node_index, "inicio"]) and self.empty_space(x=root + step, y=-self.df_nodes.loc[node_index, "fim"]):

        if self.empty_space(
            x1=root + step,
            y1=-self.df_nodes.loc[node_index, "inicio"],
            x2=root + step,
            y2=-self.df_nodes.loc[node_index, "fim"],
        ):
            new_node.set_x1(root + step)
            new_node.set_y1(-self.df_nodes.loc[node_index, "inicio"])

            new_node.set_x2(root + step)
            new_node.set_y2(-self.df_nodes.loc[node_index, "fim"])
            print("--------------------------------------------------")
            print("Node: ", new_node)
            print("X: ", root)
            print("Root: ", root)
            print("Step: ", step)
            print("--------------------------------------------------")
            return True  # put in the right

        # if self.empty_space(x=root - step, y=-self.df_nodes.loc[node_index, "inicio"]) and self.empty_space(x=root - step, y=-self.df_nodes.loc[node_index, "fim"]):

        if self.empty_space(
            x1=root - step,
            y1=-self.df_nodes.loc[node_index, "inicio"],
            x2=root - step,
            y2=-self.df_nodes.loc[node_index, "fim"],
        ):
            new_node.set_x1(root - step)
            new_node.set_y1(-self.df_nodes.loc[node_index, "inicio"])

            new_node.set_x2(root - step)
            new_node.set_y2(-self.df_nodes.loc[node_index, "fim"])
            print("--------------------------------------------------")
            print("Node: ", new_node)
            print("X: ", root)
            print("Root: ", root)
            print("Step: ", step)
            print("--------------------------------------------------")
            return True  # put in the left

        return False  # no space

    def set_nodes_coordinates(self):
        """Set the coordinates of the nodes in the graph"""
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
                while not self.try_put_node(
                    node_index=node, new_node=new_node, root=root, step=step
                ):
                    step += 1
                print(new_node)
                self.nodes_list[node] = new_node

    def set_edges_coordinates(self):
        """Set the coordinates of the edges in the graph"""
        for index, row in self.df_edges.iterrows():
            new_edge = Edge(origin_id=row["O-ID"], destination_id=row["D-ID"])

            y1 = self.nodes_list[row["D-ID"]].y1

            new_edge.set_origin_x(self.nodes_list[row["O-ID"]].x1)
            new_edge.set_origin_y(y1)

            new_edge.set_destination_x(self.nodes_list[row["D-ID"]].x1)
            new_edge.set_destination_y(y1)
            self.edges_list.append(new_edge)

    def draw(self):
        """Draw the graph"""
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

    def empty_space(self, x1, x2, y1, y2):
        """Verify if there is an node can be put in the space"""
        for node in self.nodes_list.values():
            if not node.x1 == node.x2:
                raise Exception("Node is not vertical {node}}")
            if not x1 == x2:
                raise Exception("Node is not vertical {x1, x2}")

            if node.x1 == x1 and node.x2 == x2:
                if y1 >= node.y2 or y2 <= node.y1:
                    print("--------------------------------------------------")
                    print("False: ", node)
                    return False

        print("--------------------------------------------------")
        print("line: 255")
        print("True: ", True)
        return True'''
