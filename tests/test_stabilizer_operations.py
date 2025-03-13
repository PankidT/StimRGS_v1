from stimrgs_v1.stabilizer_operations import *
import pytest

@pytest.fixture
def simulator_3arms_2bells():
    """Fixture providing initialized TableauSimulator."""
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))
    return s

@pytest.fixture
def queries_3arms_2bells():
    """Fixture providing initial queries."""
    return [
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

# @pytest.fixture
# def measurement_indices():
#     """Fixture providing measurement indices to test."""
#     return [1, 4, 7, 10]

def test_stim_rgs_3arms_2bells(queries_3arms_2bells) -> None:
    """
    For checking if the stim tableausimulator have the correct stabilizer form
    """
    s = stim_rgs_3arms_2bells()
    # Checking number of nodes
    assert s.num_qubits == 12

    queries_copy = queries_3arms_2bells.copy()

    # Check stabilizer generator
    for q in queries_copy:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    for q in queries_copy:
        if len(q) != 12:
            raise ValueError(f"Query {q} has length {len(q)}, but should have length 12.")

def test_measure_z_with_correction():
    # s, queries_mz_plus = measure_z_with_correction(index=1, s=queries_3arms_2bells, queries=queries_3arms_2bells)
    # for q in queries_mz_plus:
    #     assert s.peek_observable_expectation(stim.PauliString(q)) == 1
    pass

def test_measure_z_circuit():
    pass

def measure_y_with_correction():
    pass

def test_generate_rgs_random():
    queries, circuit = generate_rgs_random(num_nodes=16, num_bell_between_row=2)
    assert len(queries) == 16    
    for q in queries:
        assert len(q) == 16

    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit(circuit))

    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def test_find_stabilizers_result():
    pass