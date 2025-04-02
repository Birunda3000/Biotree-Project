import itertools
from enum import Enum, auto

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from IPython.display import display
from tabulate import tabulate


def create_graph(nodes: list, edges: list, label: list) -> tuple:
    """
    Creates a directed graph using the provided nodes, edges, and labels.
    Args:
        nodes (list): A list of node identifiers.
        edges (list): A list of tuples representing directed edges between nodes.
                      Each tuple is of the form (source, target).
        label (list): A list of labels corresponding to each node in the `nodes` list.
    Returns:
        tuple: A tuple containing:
            - G (networkx.DiGraph): The created directed graph.
            - lab (dict): A dictionary mapping each node to its label.
            - label_mapping (dict): A dictionary mapping each node to its label,
                                    extracted from the graph's node attributes.
    """
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
    """
    Loads a graph from two CSV files containing node and edge information.
    Args:
        path_nodes (str): The file path to the CSV file containing node data. 
                          The file should have columns "id" and "nome".
        path_edges (str): The file path to the CSV file containing edge data. 
                          The file should have columns "O-ID" and "D-ID".
    Returns:
        tuple: A tuple representing the graph, created using the `create_graph` function. 
               It includes nodes, edges, and labels.
    Notes:
        - The "id" column in the nodes file is used as the node identifiers.
        - The "nome" column in the nodes file is used as the node labels.
        - The "O-ID" and "D-ID" columns in the edges file represent the origin and destination 
          of each edge, respectively.
        - Rows with missing values in the edges file are dropped before processing.
    """
    
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
    """
    Returns the weakly connected components of a directed graph in topological order.

    This function identifies all weakly connected components in the given directed graph,
    extracts each component as a subgraph, and computes the topological order of nodes
    within each subgraph. The result is a list of lists, where each inner list contains
    the nodes of a component in topological order.

    Parameters:
        graph (networkx.DiGraph): A directed graph represented as a NetworkX DiGraph.

    Returns:
        List[List[Any]]: A list of lists, where each inner list contains the nodes of a
        weakly connected component in topological order.

    Raises:
        networkx.NetworkXUnfeasible: If the subgraph of any weakly connected component
        contains a cycle, making topological sorting impossible.
    """
    components = list(nx.weakly_connected_components(graph))
    components_in_topological_order = []
    for component in components:
        subgraph = graph.subgraph(component)
        topological_order = list(nx.topological_sort(subgraph))
        components_in_topological_order.append(topological_order)
    return components_in_topological_order


class Node:
    """
    Represents a node in a tree structure.
    Attributes:
        id (int): The unique identifier for the node.
        nome (str): The label or name of the node.
        origin (int): The origin time or starting point of the node.
        extinction (int): The extinction time or ending point of the node.
        x (Any): An optional attribute to store additional data or position, default is None.
    Methods:
        set_x(x):
            Sets the value of the `x` attribute.
        __str__() -> str:
            Returns a string representation of the node, including its id, label, origin, and extinction.
    """
    def __init__(self, id: int, label: str, origin: int, extinction: int):
        self.id = id
        self.nome = label
        self.origin = origin
        self.extinction = extinction
        self.x = None

    def set_x(self, x):
        self.x = x
    
    def get_coordinates_list(self):
        return [self.id, self.nome, self.x, self.origin, self.extinction]

    def __str__(self) -> str:
        return f"Node {self.id} - {self.nome} |Y coordenates {self.origin} - {self.extinction} |X coordenates {self.x}"


class Edge:
    """
    Represents an edge in a graph, connecting two nodes identified by their IDs.
    Attributes:
        origin_id (int): The ID of the origin node.
        destination_id (int): The ID of the destination node.
        origin_x (float): The x-coordinate of the origin node. Defaults to 0.
        origin_y (float): The y-coordinate of the origin node. Defaults to 0.
        destination_x (float): The x-coordinate of the destination node. Defaults to 0.
        destination_y (float): The y-coordinate of the destination node. Defaults to 0.
    Methods:
        set_origin_x(origin_x: float):
            Sets the x-coordinate of the origin node.
        set_origin_y(origin_y: float):
            Sets the y-coordinate of the origin node.
        set_destination_x(destination_x: float):
            Sets the x-coordinate of the destination node.
        set_destination_y(destination_y: float):
            Sets the y-coordinate of the destination node.
        __str__() -> str:
            Returns a string representation of the edge, including node IDs and coordinates.
    """
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

    def get_coordinates_list(self):
        return [
            self.origin_id,
            self.destination_id,
            self.origin_x,
            self.origin_y,
            self.destination_x,
            self.destination_y
        ]

    
    def __str__(self) -> str:
        return f"Edge IDs: {self.origin_id} - {self.destination_id} |Origin {self.origin_x} - {self.origin_y} |Destination {self.destination_x} - {self.destination_y}"


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


class Graph:
    """
    A class to represent a directed graph with nodes and edges.
    Attributes:
        label_mapping (dict): A mapping of labels for the graph components.
        components_in_topological_order (list): A list of components in topological order.
        df_nodes (DataFrame): A pandas DataFrame containing node information.
        df_edges (DataFrame): A pandas DataFrame containing edge information.
        nodes_list (dict): A dictionary of nodes in the graph, keyed by their IDs.
        edges_list (list): A list of edges in the graph.
    Methods:
        set_edges_coordinates():
            Sets the coordinates of the edges in the graph based on their origin and destination nodes.
        draw():
            Draws the graph using matplotlib, including nodes and edges.
        set_nodes_coordinates():
            Placeholder method to set the coordinates of the nodes in the graph.
        verify_space(x, y_o, y_e):
            Verifies if a node can be placed in a specific space without overlapping other nodes.
        test_verify_space():
            A test method for the `verify_space` function.
    """
    def __init__(self, label_mapping, components_in_topological_order, df_nodes, df_edges):
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
            origin = self.nodes_list[int(index)].origin
            extinction = self.nodes_list[int(index)].extinction
            x = self.find_first_available_x(y_o=origin, y_e=extinction)
            self.nodes_list[int(index)].set_x(x)

        # fill the edges_list with the info in the df_edges
        for index, row in self.df_edges.iterrows():
            self.edges_list.append(
                Edge(origin_id=row["O-ID"], destination_id=row["D-ID"])
            )

        self.set_edges_coordinates()# WARNING: Calling a method inside the constructor is not a good practice, but in this case, it is necessary to set the coordinates of the edges after creating the nodes.


    def set_edges_coordinates(self):
        """Set the coordinates of the edges in the graph"""
        for edge in self.edges_list:

            y = self.nodes_list[edge.destination_id].origin # y coordinate of the destination node

            # origin coordinates of the edge
            edge.origin_x = self.nodes_list[edge.origin_id].x
            edge.origin_y = y

            # destination coordinates of the edge
            edge.destination_x = self.nodes_list[edge.destination_id].x
            edge.destination_y = y


    def draw(self):
        """Draw the graph using matplotlib"""

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


    def get_coordinates_list(self):
        """
        Retrieves the coordinates of nodes and edges in the current structure.   
            tuple: A tuple containing two lists:
                - node_coordinates (list): A list of coordinates for all nodes in the structure. The return format is: [id, nome, x, origin, extinction] per row
                - edge_coordinates (list): A list of coordinates for all edges in the structure. The return format is: [origin_id, destination_id, origin_x, origin_y, destination_x, destination_y] per row
        """
        node_coordinates = []
        edge_coordinates = []
        for node in self.nodes_list:
            node_coordinates.append(node.get_coordinates_list())
        
        for edge in self.edges_list:
            edge_coordinates.append(edge.get_coordinates_list())

        return node_coordinates, edge_coordinates


    def print_info_table(self):
        """Prints the information of the nodes and edges in a table format."""
        nodes_headers = ["ID", "Nome", "X", "Origin", "Extinction"]
        edges_headers = ["Origin ID", "Destination ID", "Origin X", "Origin Y", "Destination X", "Destination Y"]
        
        nodes_data = [node.get_coordinates_list() for node in self.nodes_list.values()]
        edges_data = [edge.get_coordinates_list() for edge in self.edges_list]
        
        print("Nodes:")
        print(tabulate(nodes_data, headers=nodes_headers, tablefmt="grid"))
        print("\nEdges:")
        print(tabulate(edges_data, headers=edges_headers, tablefmt="grid"))


    def set_nodes_coordinates(self):
        """Set the coordinates of the nodes in the graph"""    
        for node_id in self.nodes_list:
            i=0
            print("Node ID: ", node_id)
            while not self.verify_space(x=i, y_o=self.nodes_list[node_id].origin, y_e=self.nodes_list[node_id].extinction):
                i += 1

            print(f"Node: {node_id} - {self.nodes_list[node_id].nome} |X coordenates {i}")
            self.nodes_list[node_id].set_x(i)
    

    def find_first_available_x(self, y_o, y_e):
        """
        Finds the first available x-coordinate for a new node based on its origin and extinction coordinates.
        Args:
            y_o (int): The origin y-coordinate of the new node.
            y_e (int): The extinction y-coordinate of the new node.
        Returns:
            int: The first available x-coordinate for the new node.
        """
        x = 0
        while not self.verify_space(x, y_o, y_e):
            x += 1
        return x


    def verify_space(self, x, y_o, y_e):
        """
        Verifies if there is space available on the x-coordinate for a new node 
        without overlapping with existing nodes in the nodes_list.
        Args:
            x (int): The x-coordinate to check for space.
            y_o (int): The origin y-coordinate of the new node.
            y_e (int): The extinction y-coordinate of the new node.
        Returns:
            bool: True if there is no overlap with existing nodes, False otherwise.
        """
        new_lower = min(y_o, y_e)
        new_upper = max(y_o, y_e)
        
        for node in self.nodes_list.values():
            if node.x == x:

                current_lower = min(node.origin, node.extinction)
                current_upper = max(node.origin, node.extinction)
                
                if not (new_upper < current_lower or new_lower > current_upper):
                    # There is an overlap
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
