import itertools

def is_subset(list_a: list, list_b: list) -> bool:
    """
    Check if list_a is a subset of list_b.

    Parameters:
    list_a (list): The first list to check.
    list_b (list): The second list to check against.

    Returns:
    bool: True if list_a is a subset of list_b, False otherwise.
    """
    return set(list_a).issubset(set(list_b))

def generate_combinations_with_adjustable_replacement(nodes: list, max_length: int, max_self_combination: int) -> list:
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

def find_neighbors_from_stim_tableau(index: int, queries: list) -> list:
    # Function to find neighbors based on stabilizer tableau
    neighbors = []
    for stabilizer in queries:
        # Check if the stabilizer has a sign, adjust indices accordingly
        has_sign = stabilizer[0] in ['+', '-']
        check_index = index + 1 if has_sign else index
        
        # Check if the specified index has an 'X'
        if check_index < len(stabilizer) and stabilizer[check_index] == 'X':
            for i, char in enumerate(stabilizer):
                # Skip the sign character if present
                if has_sign and i == 0:
                    continue
                    
                actual_index = i - 1 if has_sign else i
                if char == 'Z':
                    neighbors.append(actual_index)

    return neighbors

def has_edge(n_1: int, n_2: int, queries: list) -> bool:
    # Check if n_1 is a neighbor of n_2
    neighbors_of_n2 = find_neighbors_from_stim_tableau(index=n_2, queries=queries)
    return n_1 in neighbors_of_n2

def local_complementation_stim(index:int, queries:list) -> list:
    """Local complementation of the stabilizer at index."""    
    
    # Create a copy of the stabilizers to modify
    modified_stabilizers = queries.copy()
    
    neighbors = find_neighbors_from_stim_tableau(index=index, queries=queries)
    neighbors_combinations = list(itertools.combinations(neighbors, 2))

    for n_1, n_2 in neighbors_combinations:
        if has_edge(n_1, n_2, queries):
            # print(f"Removing edge between {n_1} and {n_2}")
            # Remove Z from n_1's stabilizer at position n_2
            stabilizer_n1 = list(modified_stabilizers[n_1])
            stabilizer_n1[n_2] = '_'
            modified_stabilizers[n_1] = ''.join(stabilizer_n1)
            
            # Remove Z from n_2's stabilizer at position n_1
            stabilizer_n2 = list(modified_stabilizers[n_2])
            stabilizer_n2[n_1] = '_'
            modified_stabilizers[n_2] = ''.join(stabilizer_n2)
        else:
            # print(f"Adding edge between {n_1} and {n_2}")
            # Add Z to n_1's stabilizer at position n_2
            stabilizer_n1 = list(modified_stabilizers[n_1])
            stabilizer_n1[n_2] = 'Z'
            modified_stabilizers[n_1] = ''.join(stabilizer_n1)
            
            # Add Z to n_2's stabilizer at position n_1
            stabilizer_n2 = list(modified_stabilizers[n_2])
            stabilizer_n2[n_1] = 'Z'
            modified_stabilizers[n_2] = ''.join(stabilizer_n2)    
    
    return modified_stabilizers