import stim
from stimrgs_v1.utils import *
import random

def stim_rgs_3arms_2bells() -> stim.TableauSimulator:
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))
    return s

def stim_rgs_3arms_3bells() -> stim.TableauSimulator:
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 3 0 4 0 5 1 3 1 4 1 5 2 3 2 4 2 5 6 9 6 10 6 11 7 9 7 10 7 11 8 9 8 10 8 11 3 6 4 7 5 8
    '''))
    return s

def stim_rgs_4arms_3bells() -> stim.TableauSimulator:
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        CZ 0 5 0 6 0 7 1 4 1 6 1 7 2 4 2 5 2 7 3 4 3 5 3 6 8 13 8 14 8 15 9 12 9 14 9 15 10 12 10 13 10 15 11 12 11 13 11 14 4 8 5 9 6 10 7 11
        '''))
    return s

def stim_rgs_4arms_2bells() -> stim.TableauSimulator:
    s = stim.TableauSimulator()
    s.do_circuit(
        stim.Circuit(
            """
        H 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        CZ 0 4 0 5 1 4 1 6 2 5 2 7 3 6 3 7 8 12 8 13 9 12 9 14 10 13 10 15 11 14 11 15 4 8 5 9 6 10 7 11
            """))
    return s

def verify_stim_rgs_3arms_2bells(s: stim.TableauSimulator):
    """
    check if the input (s) is correct form
    """
    # Check number of nodes
    assert s.num_qubits == 12

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

def verify_stim_rgs_3arms_3bells(s: stim.TableauSimulator):
    assert s.num_qubits == 12

    queries = [
        'X__ZZZ______', # node 0
        '_X_ZZZ______', # node 1
        '__XZZZ______', # node 2
        'ZZZX__Z_____', # node 3
        'ZZZ_X__Z____', # node 4
        'ZZZ__X__Z___', # node 5
        '___Z__X__ZZZ', # node 6
        '____Z__X_ZZZ', # node 7
        '_____Z__XZZZ', # node 8
        '______ZZZX__', # node 9
        '______ZZZ_X_', # node 10
        '______ZZZ__X'  # node 11
    ]
    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def verify_stim_rgs_4arms_3bells(s: stim.TableauSimulator):
    assert s.num_qubits == 16

    queries = [
        'X____ZZZ________', # node 0
        '_X__Z_ZZ________', # node 1
        '__X_ZZ_Z________', # node 2
        '___XZZZ_________', # node 3
        '_ZZZX___Z_______', # node 4
        'Z_ZZ_X___Z______', # node 5
        'ZZ_Z__X___Z_____', # node 6
        'ZZZ____X___Z____', # node 7
        '____Z___X____ZZZ', # node 8
        '_____Z___X__Z_ZZ', # node 9
        '______Z___X_ZZ_Z', # node 10
        '_______Z___XZZZ_', # node 11
        '_________ZZZX___', # node 12
        '________Z_ZZ_X__', # node 13
        '________ZZ_Z__X_', # node 14
        '________ZZZ____X'  # node 15
    ]
    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def verify_stim_rgs_4arms_2bells(s: stim.TableauSimulator):
    assert s.num_qubits == 16

    queries =  [
        "X___ZZ__________",  # node 0
        "_X__Z_Z_________",  # node 1
        "__X__Z_Z________",  # node 2
        "___X__ZZ________",  # node 3
        "ZZ__X___Z_______",  # node 4
        "Z_Z__X___Z______",  # node 5
        "_Z_Z__X___Z_____",  # node 6
        "__ZZ___X___Z____",  # node 7
        "____Z___X___ZZ__",  # node 8
        "_____Z___X__Z_Z_",  # node 9
        "______Z___X__Z_Z",  # node 10
        "_______Z___X__ZZ",  # node 11
        "________ZZ__X___",  # node 12
        "________Z_Z__X__",  # node 13
        "_________Z_Z__X_",  # node 14
        "__________ZZ___X",  # node 15
    ]
    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

# Improveable
def measure_z_with_correction(index:int, s:stim.TableauSimulator, queries:list) -> tuple[stim.TableauSimulator, list[str]]:

    num_nodes = s.num_qubits

    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    if index == 0:
        queries_mz_plus = [f'_{q[1:]}' for q in queries]
        queries_mz_plus[0] = 'Z' + '_'*(num_nodes-1)
    elif index == num_nodes-1:
        queries_mz_plus = [f'{q[0:num_nodes-1]}_' for q in queries]
        queries_mz_plus[num_nodes-1] = '_'*(num_nodes-1) + 'Z'
    else:
        queries_mz_plus = [f'{q[0:index]}_{q[index+1:]}' for q in queries]        
        queries_mz_plus[index] = '_'*index + 'Z' + '_'*(num_nodes-index-1)
    
    s.postselect_z(index, desired_value=False)

    for q in queries_mz_plus:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    return s, queries_mz_plus

def measure_z_circuit(circuit: str, target: int) -> str:
    input_cz = extract_numbers_after_cz(circuit)
    achive = []
    group_of_2 = []
    for i in range(len(input_cz)):
        achive.append(input_cz[i])
        if len(achive) == 2:
            group_of_2.append((achive[0], achive[1]))
            achive = []
    
    remove_target = [tup for tup in group_of_2 if target not in tup] 
    new_cz = []
    for a, b in remove_target:
        new_cz.extend([a, b])

    transformed_circuit = generate_h_cz_string(new_cz)
    # Split the transformed_circuit into lines
    lines = transformed_circuit.split('\n')
    h_line = lines[0].split()
    number_to_insert = str(target)
    h_line.append(number_to_insert)
    h_line[1:] = sorted(h_line[1:], key=int)  # Sort the numbers, excluding the first element 'H'
    lines[0] = ' '.join(h_line)
    # Reconstruct the entire string
    new_transformed_circuit = '\n'.join(lines)
    
    return new_transformed_circuit

# def measure_y_with_correction(index:int, s:stim.TableauSimulator, queries:list) -> tuple[stim.TableauSimulator, list[str]]:

#     for q in queries:
#         assert s.peek_observable_expectation(stim.PauliString(q)) == 1

#     s_validate = s.copy()

#     neighbors = find_neighbors_from_stim_tableau(index=index, stabilizers=queries)

#     # Generate new queries (side effect in select_y)
#     for neighbor in neighbors:
#         s_validate.s(neighbor)
#     queries_my_plus = s_validate.canonical_stabilizers()

#     # Apply y measurement
#     s.postselect_y(index, desired_value=False)

#     for q in queries_my_plus:
#         assert s.peek_observable_expectation(stim.PauliString(q)) == 1

#     return s, queries_my_plus 

def generate_rgs_random(num_nodes: int, num_bell_between_row: int) -> tuple[stim.TableauSimulator, list[str]]:
    """Generate a random RGS circuit with the given number of nodes and bells.
    
    Args:
        num_nodes (int): The number of nodes in the RGS system (3arms -> 12 nodes, 4arms -> 16 nodes).
        num_bell_between_row (int): The number of bells want to randomly generate between row1 and row2, as well as, row3 and row4.
    
    Returns:
        stim.TableauSimulator, list[str]
        rgs's queries from input configuration, and the generated RGS circuit as a string.
    """
    edges = []
    queries = []

    if num_nodes % 4 != 0:
        raise ValueError("Number of nodes should be a multiple of 4.")
    if num_bell_between_row > num_nodes/4:
        raise ValueError("Number of Bell pairs should be less than or equal to the number of nodes in each row.")
    
    num_nodes_each_row = int(num_nodes/4)
    row_1 = list(range(0, num_nodes_each_row))
    row_2 = list(range(num_nodes_each_row, 2*num_nodes_each_row))
    row_3 = list(range(2*num_nodes_each_row, 3*num_nodes_each_row))
    row_4 = list(range(3*num_nodes_each_row, 4*num_nodes_each_row))

    for i in range(num_nodes):
        q = ['_'] * num_nodes 
        q[i] = 'X'
        queries.append(q)

    queries_result = []
    for index, q in enumerate(queries):    

        if index in row_1:
            random_top = random.sample(row_2, num_bell_between_row)              
            for idx in random_top:
                q[idx] = 'Z'    
                queries[idx][index] = 'Z'
                edges.extend([index, idx])
        
        if index in row_2:
            # index = 2,3   z at 4,5
            # next to add z at 2,3 when index = 4,5
            q[index + num_nodes//4] = 'Z'        
                        
            edges.extend([index, index + num_nodes//4])

        if index in row_3:
            random_bottom = random.sample(row_4, num_bell_between_row)            
            for idx in random_bottom:
                q[idx] = 'Z'        
                queries[idx][index] = 'Z'  
                edges.extend([index, idx])

                q[index - num_nodes//4] = 'Z'

        q = ''.join(q)
        queries_result.append(q)
        circuit = generate_h_cz_string(edges, fix_nodes=True, num_nodes=num_nodes)
        s = stim.TableauSimulator()
        s.do_circuit(stim.Circuit(circuit))

        for q in queries_result:
            assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    return queries_result, circuit
   
def find_stabilizers_result(num_nodes:int):
    all_stabilizer_result = []
    num_nodes_each_row = int(num_nodes/4)
    row_1 = list(range(0, num_nodes_each_row))
    row_2 = list(range(num_nodes_each_row, 2*num_nodes_each_row))
    row_3 = list(range(2*num_nodes_each_row, 3*num_nodes_each_row))
    row_4 = list(range(3*num_nodes_each_row, 4*num_nodes_each_row))

    for i in row_1:
        for j in row_2:
            for k in row_3:
                for l in row_4:
                    # Create s_1 and replace character at index j with 'Z'
                    s_1 = '_' * i + 'X' + '_' * (num_nodes -1 -i) 
                    s_1 = s_1[:j] + 'Z' + s_1[j+1:]  # Create a new string with 'Z' at the desired position                

                    # Create s_2 and replace character at index k with 'Z'
                    s_2 = '_' * j + 'X' + '_' * (num_nodes -1 - j)
                    s_2 = s_2[:k] + 'Z' + s_2[k+1:]  # Create a new string with 'Z' at the desired position
                    # Create a new string with 'Z' at the desired index i
                    s_2 = s_2[:i] + 'Z' + s_2[i+1:]  # Replace character at index i with 'X'

                    s_3 = '_' * k + 'X' + '_' * (num_nodes -1 - k)
                    s_3 = s_3[:l] + 'Z' + s_3[l+1:]  
                    # Create a new string with 'Z' at the desired position
                    s_3 = s_3[:j] + 'Z' + s_3[j+1:]  # Replace character at index i with 'X'

                    s_4 = '_' * l + 'X' + '_' * (num_nodes -1 - l)
                    s_4 = s_4[:k] + 'Z' + s_4[k+1:]  # Create a new string with 'Z' at the desired position

                    stabilizer_result = [s_1, s_2, s_3, s_4]
                    all_stabilizer_result.append(stabilizer_result)

    if len(all_stabilizer_result) != ((num_nodes//4)**4):
        raise ValueError("The number of stabilizer strings is not correct")
    
    return all_stabilizer_result