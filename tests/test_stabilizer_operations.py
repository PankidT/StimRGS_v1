from stimrgs_v1.stabilizer_operations import *
import pytest

@pytest.fixture
def simulator():
    """Fixture providing initialized TableauSimulator."""
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))
    return s

@pytest.fixture
def queries():
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

@pytest.fixture
def measurement_indices():
    """Fixture providing measurement indices to test."""
    return [1, 4, 7, 10]

def test_stim_rgs_3arms(queries) -> None:
    """
    For checking if the stim tableausimulator have the correct stabilizer form
    """
    s = stim_rgs_3arms_2bells()
    # Checking number of nodes
    assert len(s.current_inverse_tableau()) == 12

    queries_copy = queries.copy()

    # Check stabilizer generator
    for q in queries_copy:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def test_measure_z_with_correction_loop(simulator, queries, measurement_indices):
    """Test measure_z_with_correction using a loop approach."""
    s = simulator
    queries_copy = queries.copy()  # Create a copy to avoid modifying the fixture
    
    for idx in measurement_indices:
        s, queries_copy = measure_z_with_correction(index=idx, s=s, queries=queries_copy)
    
    for q in queries_copy:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def test_measure_z_with_correction_individual(simulator, queries, measurement_indices):
    """Test measure_z_with_correction with individual calls."""
    s = simulator
    queries_copy = queries.copy()  # Create a copy to avoid modifying the fixture
    
    # Apply each measurement individually 
    for idx in measurement_indices:
        s, queries_copy = measure_z_with_correction(index=idx, s=s, queries=queries_copy)
    
    for q in queries_copy:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1