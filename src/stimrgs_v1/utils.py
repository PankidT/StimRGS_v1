import itertools
import re
import stim

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

def fast_generate_combinations_with_adjustable_replacement(nodes: list, max_length: int, max_self_combination: int) -> list:
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
    if max_self_combination >= max_length:
        # If max_self_combination is >= max_length, just use the standard function
        return list(itertools.combinations_with_replacement(nodes, max_length))
    
    # Use recursive generation with pruning
    result = []
    
    def backtrack(current, start_idx, remaining):
        if remaining == 0:
            result.append(tuple(current))
            return
        
        for i in range(start_idx, len(nodes)):
            # Count how many times the current element is already in the combination
            count = current.count(nodes[i])
            
            # Only add if we haven't reached the maximum allowed repetitions
            if count < max_self_combination:
                current.append(nodes[i])
                # Stay at the same index for the next recursion since we can reuse elements
                backtrack(current, i, remaining - 1)
                current.pop()
    
    backtrack([], 0, max_length)
    return result

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

def find_neighbors_from_selected_node(input_list: list, selected_node: int) -> list:
    # Create a list of tuples from consecutive pairs of elements
    grouped_elements = [(input_list[i], input_list[i+1]) for i in range(0, len(input_list) - 1, 2)]
    
    neighbors = []
    for edge in grouped_elements:
        if edge[0] == selected_node:
            neighbors.append(edge[1])
        elif edge[1] == selected_node:
            neighbors.append(edge[0])

    return neighbors

def has_edge(n_1: int, n_2: int, queries: list) -> bool:
    # Check if n_1 is a neighbor of n_2
    neighbors_of_n2 = find_neighbors_from_stim_tableau(index=n_2, queries=queries)
    return n_1 in neighbors_of_n2

def extract_numbers_after_cz(input_string):
    # Use regular expression to find numbers after "CZ"
    match = re.search(r'CZ\s+([\d\s]+)', input_string)
    if match:
        # Extract the numbers and convert them to a list of integers
        numbers = list(map(int, match.group(1).split()))
        return numbers
    else:
        return []
    
def filter_groups(numbers, filter_tuples):    
    # Create groups of 2
    groups = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers)-1)]
    
    # Convert groups and filter_tuples to sets for efficient comparison
    groups_set = set(groups)
    filter_set = set(filter_tuples)
    
    # Remove tuples that exist in both groups and filter
    groups_set -= groups_set.intersection(filter_set)
    
    # Add tuples from filter that are not in original groups
    groups_set.update(filter_set - set(groups))

    lst = sorted(list(groups_set))
    lst = [tpl for tpl in lst if tpl[0] != tpl[1]]
    result = []
    for a, b in lst:
        result.extend([a, b])

    achive = []
    filtered_result = []
    for i in range(len(result)):
        achive.append(result[i])
        if len(achive) == 2:
            if achive[0] < achive[1]:
                filtered_result.append((achive[0], achive[1]))
                achive = []
            else:
                achive = []

    final_result = []
    for a, b in filtered_result:
        final_result.extend([a, b])

    # Convert back to list and sort for consistent output
    return final_result

def generate_h_cz_string(numbers: list, fix_nodes: bool=False, num_nodes: int=None) -> str:    
    if fix_nodes:
        unique_numbers = [i for i in range(num_nodes)]
        h_line = "H " + " ".join(map(str, sorted(unique_numbers)))
        cz_line = "CZ " + " ".join(map(str, numbers))
    else:
        unique_numbers = sorted(set(numbers), key=numbers.index)
        h_line = "H " + " ".join(map(str, sorted(unique_numbers)))
        cz_line = "CZ " + " ".join(map(str, numbers))
    return f"""{h_line}\n{cz_line}"""

def local_complementation_stim(index:int, queries:list, circuit:str) -> tuple[stim.TableauSimulator, list[str], str]:
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

    original_cz = extract_numbers_after_cz(circuit)
    cz_after_filtered = filter_groups(original_cz, neighbors_combinations)
    # print(f'original_cz: {original_cz}')
    # print(f'neighbors_combinations: {neighbors_combinations}')
    # print(f'cz_after_filtered: {cz_after_filtered}')
    # print('- - - - - - - - - - - - - - - - - - - - - - - -')
    circuit_string = generate_h_cz_string(cz_after_filtered)
    
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit(circuit_string))
    
    return s, modified_stabilizers, circuit_string