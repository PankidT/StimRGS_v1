import itertools
import random
import networkx as nx
from networkx import Graph

def local_complementation(graph: Graph, target: int) -> Graph:
    # Get the neighbors of the target node
    neighbors = list(graph.neighbors(target))

    neighbors_combinations = list(itertools.combinations(neighbors, 2))

    G = graph.copy()
    for neighbor1, neighbor2 in neighbors_combinations:
        if G.has_edge(neighbor1, neighbor2):
            G.remove_edge(neighbor1, neighbor2) # Remove edge if it exists
        else:
            G.add_edge(neighbor1, neighbor2) # Add edge if it does not exist        
            
    return G

def z_measure(graph: Graph, target: int) -> Graph:    
    graph.remove_node(target)
    graph.add_node(target)

def y_measure(graph: Graph, target: int) -> Graph:
    local_complementation(graph, target)
    z_measure(graph, target)

def x_measure(graph: Graph, target: int) -> Graph:    
    if list(graph.neighbors(target)) == []:
        return
    else: 
        neighbors = list(graph.neighbors(target))

    selected_neighbors = random.choice(neighbors)

    local_complementation(graph, selected_neighbors)
    y_measure(graph, target)
    local_complementation(graph, selected_neighbors)
    
def check_subgraph(main_graph:Graph, subgraph:Graph) -> bool:
    
    for node in subgraph.nodes():
        # Get ALL neighbors in main graph
        main_neighbors = set(main_graph.neighbors(node))
        # Get neighbors in subgraph
        sub_neighbors = set(subgraph.neighbors(node))
        
        # print(f"Node {node}:")
        # print(f"  ALL neighbors in main graph: {main_neighbors}")
        # print(f"  Neighbors in subgraph: {sub_neighbors}")
        
        # If this node has ANY additional connections in main graph, return False
        if main_neighbors == sub_neighbors:
            # print(f"  Node {node} has extra connections in main graph")
            continue
        else:
            return False
    
    return True

def validate_result(current_graph: Graph, container: list):
    bell_pairs_1 = []

    # Define the main nodes and edges
    base_nodes = [3, 6]

    # Iterate over the conditions
    for i in range(3):  # For nodes 0, 1, 2
        for j in range(3):  # For nodes 9, 10, 11
            # Create a new graph
            bell_pair = Graph()
            # Add nodes
            bell_pair.add_nodes_from([i, *base_nodes, 9 + j])
            # Add edges
            bell_pair.add_edges_from([(i, 3), (3, 6), (6, 9 + j)])
            # Append the graph to the list
            bell_pairs_1.append(bell_pair)

    bell_pairs_2 = []

    # Define the main nodes and edges
    base_nodes = [5, 8]

    # Iterate over the conditions
    for i in range(3):  # For nodes 0, 1, 2
        for j in range(3):  # For nodes 9, 10, 11
            # Create a new graph
            bell_pair = Graph()
            # Add nodes
            bell_pair.add_nodes_from([i, *base_nodes, 9 + j])
            # Add edges
            bell_pair.add_edges_from([(i, 5), (5, 8), (8, 9 + j)])
            # Append the graph to the list
            bell_pairs_2.append(bell_pair)

    for bell_pair_i in bell_pairs_1:
        for bell_pair_j in bell_pairs_2:
            if (check_subgraph(current_graph, bell_pair_i) and check_subgraph(current_graph, bell_pair_j)):
                result_G = current_graph.copy()
                container.append(result_G)
                return True
            else:
                continue

def generate_combinations_with_adjustable_replacement(nodes, max_length, max_self_combination):
    """
    Generate combinations of exactly max_length elements from nodes,
    where each element can appear up to max_self_combination times.
    
    Args:
        nodes: List of nodes to generate combinations from
        max_length: Exact length of combinations to generate
        max_self_combination: Maximum number of times an element can appear in a combination
    
    Returns:
        List of tuples containing the combinations
    """
    # Generate combinations with replacement of exactly max_length
    combinations = itertools.combinations_with_replacement(nodes, max_length)
    
    # Filter combinations based on max_self_combination constraint
    filtered_combinations = [
        combo for combo in combinations 
        if all(combo.count(x) <= max_self_combination for x in set(combo))
    ]
    
    return filtered_combinations