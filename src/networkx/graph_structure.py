import networkx as nx
import random
import matplotlib.pyplot as plt
from networkx import Graph

class LinearGraph:
    def __init__(self, n_nodes: int):
        """Initialize a linear graph with n_nodes."""
        self.graph = Graph()

        # Add nodes
        self.nodes = list(range(n_nodes))
        self.graph.add_nodes_from(self.nodes)

        # Add edges
        self.edges = [(i, i+1) for i in range(n_nodes-1)]
        self.graph.add_edges_from(self.edges)

class StarGraph:
    def __init__(self, num_vertices: int=5):
        """
        Initialize a star graph with specified number of vertices.
        The center vertex is always node 0, with peripheral nodes numbered 1 to n-1.
        
        Args:
            num_vertices (int): Total number of vertices (must be >= 2)
        """
        if num_vertices < 2:
            raise ValueError("Star graph must have at least 2 vertices")
            
        self.graph = Graph()
        self.num_vertices = num_vertices
        
        # Add nodes
        self.nodes = list(range(num_vertices))
        self.graph.add_nodes_from(self.nodes)
        
        # Add edges (connect all peripheral nodes to center node 0)
        self.edges = [(0, i) for i in range(1, num_vertices)]
        self.graph.add_edges_from(self.edges)
        
        # Center node is node 0
        self.center_node = 0
        
        # Peripheral nodes are all other nodes
        self.peripheral_nodes = set(range(1, num_vertices))

class RGSGraph:
    def __init__(self):
        """Initialize an RGS graph with predefined structure."""
        self.graph = Graph()
        
        # Add nodes
        self.nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.graph.add_nodes_from(self.nodes)
        
        # Add edges
        self.edges = [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5),
                     (2, 3), (2, 4), (2, 5), (6, 9), (6, 10), (6, 11),
                     (7, 9), (7, 10), (7, 11), (8, 9), (8, 10), (8, 11),
                     (3, 6), (5, 8)]
        self.graph.add_edges_from(self.edges)     

        self.pos = {
                    # Top row (Alice)
                    0: (0, 3),
                    1: (1.5, 3),
                    2: (3, 3),
                    
                    # Second row (ABSA)
                    3: (0, 2),
                    4: (1.5, 2),
                    5: (3, 2),
                    
                    # Third row (Bob)
                    6: (0, 1),
                    7: (1.5, 1),
                    8: (3, 1),
                    
                    # Bottom row
                    9: (0, 0),
                    10: (1.5, 0),
                    11: (3, 0)
                }   

    def reset_graph(self):
        """Reset the graph to its initial state."""
        self.graph.clear()
        self.graph.add_edges_from(
            [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5),
                (2, 3), (2, 4), (2, 5), (6, 9), (6, 10), (6, 11),
                (7, 9), (7, 10), (7, 11), (8, 9), (8, 10), (8, 11),
                (3, 6), (5, 8)]
        )

class RGSGraph_incomplete:
    def __init__(self):
        """Initialize an RGS graph with predefined structure."""
        self.graph = Graph()
        
        # Add nodes
        self.nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.graph.add_nodes_from(self.nodes)
        
        # Add edges
        self.edges = [(0, 4), (0, 5), (1, 3), (1, 5),
                     (2, 3), (2, 4), (6, 10), (6, 11),
                     (7, 9), (7, 11), (8, 9), (8, 10),
                     (3, 6), (4,7),(5, 8)]
        self.graph.add_edges_from(self.edges)        

        self.pos = {
                    # Top row (Alice)
                    0: (0, 3),
                    1: (1.5, 3),
                    2: (3, 3),
                    
                    # Second row (ABSA)
                    3: (0, 2),
                    4: (1.5, 2),
                    5: (3, 2),
                    
                    # Third row (Bob)
                    6: (0, 1),
                    7: (1.5, 1),
                    8: (3, 1),
                    
                    # Bottom row
                    9: (0, 0),
                    10: (1.5, 0),
                    11: (3, 0)
                }   

    def reset_graph(self):
        """Reset the graph to its initial state."""
        self.graph.clear()
        self.graph.add_edges_from(
            [(0, 4), (0, 5), (1, 3), (1, 5),
                (2, 3), (2, 4), (6, 10), (6, 11),
                (7, 9), (7, 11), (8, 9), (8, 10),
                (3, 6), (5, 8)]
        )

class RGSGraph_incomplete_2:
    def __init__(self):
        """Initialize an RGS graph with predefined structure."""
        self.graph = Graph()
        
        # Add nodes
        self.nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.graph.add_nodes_from(self.nodes)
        
        # Add edges
        self.edges = [(0, 4), (0, 5), (1, 3), (1, 5),
                     (2, 3), (2, 4), (6, 10), (6, 11),
                     (7, 9), (7, 11), (8, 9), (8, 10),
                     (3, 6), (4, 7)]
        self.graph.add_edges_from(self.edges)        

        self.pos = {
                    # Top row (Alice)
                    0: (0, 3),
                    1: (1.5, 3),
                    2: (3, 3),
                    
                    # Second row (ABSA)
                    3: (0, 2),
                    4: (1.5, 2),
                    5: (3, 2),
                    
                    # Third row (Bob)
                    6: (0, 1),
                    7: (1.5, 1),
                    8: (3, 1),
                    
                    # Bottom row
                    9: (0, 0),
                    10: (1.5, 0),
                    11: (3, 0)
                }   

    def reset_graph(self):
        """Reset the graph to its initial state."""
        self.graph.clear()
        self.graph.add_edges_from(
            [(0, 4), (0, 5), (1, 3), (1, 5),
                (2, 3), (2, 4), (6, 10), (6, 11),
                (7, 9), (7, 11), (8, 9), (8, 10),
                (3, 6), (4, 7)]
        )

class FourArmsRGS_remove_1_edge:
    def __init__(self):
        self.nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.pos = {
            # Top row (Alice)
            0: (0, 3),
            1: (1.5, 3),
            2: (3, 3),
            3: (4.5, 3),
            
            # Second row (ABSA)
            4: (0, 2),
            5: (1.5, 2),
            6: (3, 2),
            7: (4.5, 2),

            # Third row
            8: (0, 1),
            9: (1.5, 1),
            10: (3, 1),
            11: (4.5, 1),

            # Fourth row
            12: (0, 0),
            13: (1.5, 0),
            14: (3, 0),
            15: (4.5, 0)
        }
        self.graph = Graph()
        self.graph.add_nodes_from(self.nodes)

        for node in [0, 1, 2, 3]:
            if node == 0:
                self.graph.add_edges_from([(node, 5), (node, 6), (node, 7)])
            elif node == 1:
                self.graph.add_edges_from([(node, 4), (node, 6), (node, 7)])
            elif node == 2:
                self.graph.add_edges_from([(node, 4), (node, 5), (node, 7)])
            elif node == 3:
                self.graph.add_edges_from([(node, 4), (node, 5), (node, 6)])

        for node in [8, 9, 10, 11]:
            if node == 8:
                self.graph.add_edges_from([(node, 13), (node, 14), (node, 15)])
            elif node == 9:
                self.graph.add_edges_from([(node, 12), (node, 14), (node, 15)])
            elif node == 10:
                self.graph.add_edges_from([(node, 12), (node, 13), (node, 15)])
            elif node == 11:
                self.graph.add_edges_from([(node, 12), (node, 13), (node, 14)])

        # Bell pairs
        self.graph.add_edges_from([(4, 8), (7, 11)])

    def reset_graph(self):
        self.graph.clear()
        self.graph.add_nodes_from(self.nodes)

        for node in [0, 1, 2, 3]:
            if node == 0:
                self.graph.add_edges_from([(node, 5), (node, 6), (node, 7)])
            elif node == 1:
                self.graph.add_edges_from([(node, 4), (node, 6), (node, 7)])
            elif node == 2:
                self.graph.add_edges_from([(node, 4), (node, 5), (node, 7)])
            elif node == 3:
                self.graph.add_edges_from([(node, 4), (node, 5), (node, 6)])

        for node in [8, 9, 10, 11]:
            if node == 8:
                self.graph.add_edges_from([(node, 13), (node, 14), (node, 15)])
            elif node == 9:
                self.graph.add_edges_from([(node, 12), (node, 14), (node, 15)])
            elif node == 10:
                self.graph.add_edges_from([(node, 12), (node, 13), (node, 15)])
            elif node == 11:
                self.graph.add_edges_from([(node, 12), (node, 13), (node, 14)])

        # Bell pairs
        self.graph.add_edges_from([(4, 8), (7, 11)])

    def draw(self):
        plt.figure(figsize=(7, 6))
        nx.draw(self.graph, self.pos, with_labels=True)
        plt.title("RGS with one edge removed")
        plt.show()


class FourArmsRGS_half_complete:
    def __init__(self, draw: bool = False):
        self.graph = Graph()
        self.copy_graph = self.graph.copy()

        self.nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.pos = {
            # Top row (Alice)
            0: (0, 3),
            1: (1.5, 3),
            2: (3, 3),
            3: (4.5, 3),
            
            # Second row (ABSA)
            4: (0, 2),
            5: (1.5, 2),
            6: (3, 2),
            7: (4.5, 2),

            # Third row
            8: (0, 1),
            9: (1.5, 1),
            10: (3, 1),
            11: (4.5, 1),

            # Fourth row
            12: (0, 0),
            13: (1.5, 0),
            14: (3, 0),
            15: (4.5, 0)
        }

        self.graph.add_nodes_from(self.nodes)

        second_row = [4, 5, 6, 7]
        fouth_row = [12, 13, 14, 15]      

        for node in [0, 1, 2, 3]:
            if node == 0:
                first_link = random.choice(second_row)
                while True:
                    second_link = random.choice(second_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

            elif node == 1:
                first_link = random.choice(second_row)
                while True:
                    second_link = random.choice(second_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

            elif node == 2:
                first_link = random.choice(second_row)
                while True:
                    second_link = random.choice(second_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

            elif node == 3:
                first_link = random.choice(second_row)
                while True:
                    second_link = random.choice(second_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

        for node in [8, 9, 10, 11]:
            if node == 8:
                first_link = random.choice(fouth_row)
                while True:
                    second_link = random.choice(fouth_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

            elif node == 9:
                first_link = random.choice(fouth_row)
                while True:
                    second_link = random.choice(fouth_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

            elif node == 10:
                first_link = random.choice(fouth_row)
                while True:
                    second_link = random.choice(fouth_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

            elif node == 11:
                first_link = random.choice(fouth_row)
                while True:
                    second_link = random.choice(fouth_row)
                    if second_link != first_link:
                        break
                self.graph.add_edges_from([(node, first_link), (node, second_link)])

        

    def create_bell_pairs(self, rand=True, num_bells=2):
        if rand:
            for i in range(num_bells):
            
                second_row = random.choice([4, 5, 6, 7])
                third_row = random.choice([8, 9, 10, 11])

                self.graph.add_edges_from([(second_row, third_row)])    
        else:
            self.graph.add_edges_from([(4, 8), (7, 11)])

    def reset_graph(self):
        self.graph.clear()
        self.graph = self.copy_graph.copy()

    def draw(self):
        plt.figure(figsize=(7, 6))
        nx.draw(self.graph, self.pos, with_labels=True)
        plt.title("Incomplete RGS with half-complete edges")
        plt.show()