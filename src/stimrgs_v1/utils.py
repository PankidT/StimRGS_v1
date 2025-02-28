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