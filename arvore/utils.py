import itertools
from enum import Enum, auto

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from IPython.display import display
from tabulate import tabulate
import math
import copy


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

        # Create nodes in the order of the components
        # This ensures that the nodes are created in the order of their topological components
        for pos, node_id in enumerate(flattened_list):
            row = self.df_nodes.loc[node_id]
            self.nodes_list[int(node_id)] = Node(
                id=int(node_id),
                label=row["nome"],
                origin=int(-row["inicio"]),
                extinction=int(-row["fim"]),
                )
            origin = self.nodes_list[int(node_id)].origin
            extinction = self.nodes_list[int(node_id)].extinction
            x = self.find_first_available_x(y_o=origin, y_e=extinction)
            self.nodes_list[int(node_id)].set_x(x)

        # Uncomment the following lines if you want to use the original method of filling nodes_list
        '''for index, row in self.df_nodes.iterrows():
            self.nodes_list[int(index)] = Node(
                id=int(index),
                label=row["nome"],
                origin=int(-row["inicio"]),
                extinction=int(-row["fim"]),
            )
            origin = self.nodes_list[int(index)].origin
            extinction = self.nodes_list[int(index)].extinction
            x = self.find_first_available_x(y_o=origin, y_e=extinction)
            self.nodes_list[int(index)].set_x(x)'''

        # fill the edges_list with the info in the df_edges
        for index, row in self.df_edges.iterrows():
            self.edges_list.append(
                Edge(origin_id=row["O-ID"], destination_id=row["D-ID"])
            )

        self.set_edges_coordinates()# WARNING: Calling a method inside the constructor is not a good practice, but in this case, it is necessary to set the coordinates of the edges after creating the nodes.


    def purge_node_positions(self):
        """
        Resets the x-coordinate positions of all nodes in the graph.

        This method iterates through all nodes in the `nodes_list` and sets their
        `x` attribute to `None`, effectively purging any previously assigned
        x-coordinate values.

        Returns:
            None
        """
        for node in self.nodes_list.values():
            node.x = None


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
                head_width=0.2,
                head_length=0.2,
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


    def calculate_crossings(self):
        """
        Calculate the number of crossings between edges and nodes in the tree structure.
        This method iterates through all edges in the `edges_list` and checks if any node's
        vertical bar intersects with the horizontal line segment defined by the edge. A crossing
        is counted if the node's vertical bar overlaps the edge's horizontal line segment.
        Returns:
            int: The total number of crossings detected.
        """
        crossings = 0
        for edge in self.edges_list:
            # Define the horizontal edge line: from x_origin to x_destination, at height y = y_edge
            x_start = edge.origin_x
            x_end = edge.destination_x
            y_edge = edge.origin_y  # Destination is defined with y equal to the origin of the descendant

            # Ensure x_start is the smallest
            if x_start > x_end:
                x_start, x_end = x_end, x_start

            # Check each node that is neither the origin nor the destination
            for node in self.nodes_list.values():
                if node.id in [edge.origin_id, edge.destination_id]:
                    continue
                # If the node is in the same vertical range (overlapping the edge line)
                node_lower = min(node.origin, node.extinction)
                node_upper = max(node.origin, node.extinction)
                if node_lower <= y_edge <= node_upper:
                    # If the node is between x_start and x_end, we consider that the edge crosses the node's bar
                    if x_start < node.x < x_end:
                        crossings += 1


                        print(f"Crossing detected: Edge {edge.origin_id} -> {edge.destination_id} crosses Node {node.id} at x={node.x}, y={y_edge}")#debug

        return crossings


    def calculate_sum_vector_lengths(self):
        """
        Calculates the sum of the horizontal distances (vector magnitudes) 
        between related nodes in a tree structure.

        For each edge in the tree, the magnitude is computed as the absolute 
        difference between the x-coordinates of the ancestor (origin) and 
        descendant (destination). Minimizing this value helps group ancestors 
        and descendants closer together.

        Returns:
            float: The total sum of the horizontal distances for all edges.
        """
        total_length = 0
        for edge in self.edges_list:
            length = abs(edge.destination_x - edge.origin_x)
            total_length += length
        
        print(f"Total length of vectors: {total_length}")#debug
        return total_length


    def calculate_overlaps(self):
        """
        Calculate a penalty for overlapping ancestral relationship vectors.

        This method evaluates pairs of edges in the `edges_list` to determine if they overlap
        based on their vertical (y-axis) proximity and horizontal (x-axis) intervals. If two edges
        have y-coordinates within a specified tolerance (`delta_y`) and their x-coordinate intervals
        overlap, a penalty is added.

        Returns:
            int: The total overlap penalty, where each overlapping pair of edges contributes to the penalty.
        """
        overlap_penalty = 0
        delta_y = 0.5  # Vertical tolerance to consider that two edges "overlap"
        for edge1, edge2 in itertools.combinations(self.edges_list, 2):
            # Consider the y-coordinates of the vectors: we use the y of the destination (origin of the descendant)
            y1 = edge1.origin_y
            y2 = edge2.origin_y
            if abs(y1 - y2) < delta_y:
                # Check for overlap on the x-axis: if the intervals [min(x1,x2), max(x1,x2)] overlap
                x1_min, x1_max = sorted([edge1.origin_x, edge1.destination_x])
                x2_min, x2_max = sorted([edge2.origin_x, edge2.destination_x])
                # If there is an intersection of the interval
                if not (x1_max < x2_min or x2_max < x1_min):
                    # Penalize; the greater the overlap, the higher the penalty
                    overlap_penalty += 1
                    print(f"Overlap detected: Edge {edge1.origin_id} -> {edge1.destination_id} overlaps with Edge {edge2.origin_id} -> {edge2.destination_id}")#debug

        return overlap_penalty


    def calculate_layout_quality(self, w1=3, w2=1, w3=6):
        """
        Calculate the quality of the layout based on crossings, vector lengths, and overlaps.
        The quality is computed as a weighted negative sum of the following factors:
        - Number of crossings (calculated using `calculate_crossings`).
        - Sum of vector lengths (calculated using `calculate_sum_vector_lengths`).
        - Number of overlaps (calculated using `calculate_overlaps`).
        Parameters:
            w1 (float): Weight for the crossings factor. Default is 3.
            w2 (float): Weight for the sum of vector lengths factor. Default is 1.
            w3 (float): Weight for the overlaps factor. Default is 6.
        Returns:
            float: The calculated quality of the layout. A lower value indicates a better layout.
        """
        crossings = self.calculate_crossings()
        sum_lengths = self.calculate_sum_vector_lengths()
        overlaps = self.calculate_overlaps()

        n_edges = len(self.edges_list)
        
        normalized_crossings = crossings / n_edges if n_edges > 0 else 0
        normalized_sum_lengths = sum_lengths / n_edges if n_edges > 0 else 0
        # logarithmically normalize the overlaps
        normalized_overlaps = math.log(1 + overlaps)


        # multiply by -1 to make bigger quality better, the maximum quality is 0
        quality = - (w1 * normalized_crossings + w2 * normalized_sum_lengths + w3 * normalized_overlaps)

        print(f"first component: {normalized_crossings} * {w1} = {normalized_crossings * w1}")
        print(f"second component: {normalized_sum_lengths} * {w2} = {normalized_sum_lengths * w2}")
        print(f"third component: {normalized_overlaps} * {w3} = {normalized_overlaps * w3}")
        print(f"Quality: {quality}")

        return quality
    
    def get_current_solution(self):
        """
        Retrieves the current solution based on the nodes in the nodes_list.

        This method iterates through the nodes_list dictionary, checks if each node
        has a non-None value for its 'x' attribute, and collects the node ID along
        with the 'x' value into a list.

        Returns:
            list: A list of tuples where each tuple contains a node ID and its 
                  corresponding 'x' value for nodes with a non-None 'x' attribute.
        """
        solution = []
        for node_id, node in self.nodes_list.items():
            if node.x is not None:
                solution.append((node_id, node.x))
        return solution





def evaluate_possible_solution(nodes_posicions_list, graph):
    """
    Evaluate a possible solution for the graph layout based on the given node positions.
    This function calculates the quality of the layout using the `calculate_layout_quality` method, without
    modifying the original graph. It uses the provided node positions to create a new graph instance for evaluation.
    If the posicioning is not valid, it returns false not the quality.

    Parameters:
        nodes_posicions_list (list): A list of tuples representing the x-coordinates for each node.
                                      Each tuple contains (node_id, x_coordinate).
        graph (Graph): The graph object to evaluate.

    Returns:
        float or bool: The quality of the layout if the positioning is valid, otherwise False.

    """
    graph_copy = copy.deepcopy(graph)  # Create a deep copy of the graph to avoid modifying the original
    graph_copy.purge_node_positions()  # Clear existing node positions in the copy

    for node_id, x in nodes_posicions_list:

        if node_id not in graph_copy.nodes_list:
            print(f"Node {node_id} not found in the graph.")
            return False

        
        if graph_copy.verify_space(x, graph_copy.nodes_list[node_id].origin, graph_copy.nodes_list[node_id].extinction):
            graph_copy.nodes_list[node_id].set_x(x)
        else:
            print(f"Invalid positioning for node {node_id} at x={x}.")
            return False
    
    graph_copy.set_edges_coordinates()  # Set edge coordinates based on the new node positions
    quality = graph_copy.calculate_layout_quality()  # Calculate the layout quality


    graph_copy.draw()  # Draw the graph with the new layout


    return quality  # Return the quality of the layout



def generate_random_solution():
    """
    Generates a random solution for the graph layout.

    This function creates a random permutation of x-coordinates for the nodes in the graph.
    It ensures that the x-coordinates are unique and within a specified range.

    Returns:
        list: A list of tuples where each tuple contains a node ID and its randomly assigned x-coordinate.
    """
    # Generate a random permutation of x-coordinates
    x_coordinates = list(range(1, len(graph.nodes_list) + 1))
    random.shuffle(x_coordinates)
    
    # Create a list of tuples (node_id, x_coordinate)
    nodes_posicions_list = [(node_id, x) for node_id, x in zip(graph.nodes_list.keys(), x_coordinates)]
    
    return nodes_posicions_list