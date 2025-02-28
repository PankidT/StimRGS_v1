import stim
import itertools

def stim_rgs_3arms() -> stim.TableauSimulator:
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))
    return s

def test_stim_rgs_3arms(s: stim.TableauSimulator):
    """
    check if the input (s) is correct form
    """
    # Check number of nodes
    assert len(s.current_inverse_tableau()) == 12

    queries = [
        'X___ZZ______', # node 0
        '_X_Z_Z______', # node 1
        '__XZZ_______', # node 2
        '_ZZX__Z_____', # node 3
        'Z_Z_X__Z____', # node 4
        'ZZ___X__Z___', # node 5
        '___Z__X___ZZ', # node 6
        '____Z__X_Z_Z', # node 7
        '_____Z__XZZ_', # node 8
        '_______ZZX__', # node 9
        '______Z_Z_X_', # node 10
        '______ZZ___X'  # node 11
    ]
    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def measure_z_with_correction(index:int, s:stim.TableauSimulator, queries:list) -> stim.TableauSimulator:

    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    if index == 0:
        queries_mz_plus = [f'_{q[1:]}' for q in queries]
        queries_mz_plus[0] = 'Z___________'
    elif index == 11:
        queries_mz_plus = [f'{q[0:11]}_' for q in queries]
        queries_mz_plus[11] = '___________Z'
    else:
        queries_mz_plus = [f'{q[0:index]}_{q[index+1:]}' for q in queries]        
        queries_mz_plus[index] = '_'*index + 'Z' + '_'*(11-index)

    s.postselect_z(index, desired_value=False) 

    for q in queries_mz_plus:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    return s, queries_mz_plus

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