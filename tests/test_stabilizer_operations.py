from stimrgs_v1.stabilizer_operations import *
import pytest

@pytest.fixture
def RGS_3arms_queries():
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
def RGS_3arms_circuit():
    s = stim.TableauSimulator()
    return s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))

def test_stim_rgs_3arms(RGS_3arms_queries) -> None:
    """
    For checking if the stim tableausimulator have the correct stabilizer form
    """
    s = stim_rgs_3arms()
    # Checking number of nodes
    assert len(s.current_inverse_tableau()) == 12

    # Check stabilizer generator
    for q in RGS_3arms_queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def test_mesure_z_with_correction() -> None:
    """
    Input: measurement_index, TableauSimulator, ini_queries
    Output TableauSimulator, update_queries
    """

    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))

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

    measurement_index = [1,4,7,10]

    # loop over measurement_index
    for i in measurement_index:
        s, queries = measure_z_with_correction(index=i, s=s, queries=queries)
        for q in queries:
            assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    # line by line measurement
    s = stim.TableauSimulator()
    s.do_circuit(stim.Circuit('''
        H 0 1 2 3 4 5 6 7 8 9 10 11
        CZ 0 4 0 5 1 3 1 5 2 3 2 4 6 10 6 11 7 9 7 11 8 9 8 10 3 6 4 7 5 8    
    '''))

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
    s, queries = measure_z_with_correction(index=1, s=s, queries=queries)
    s, queries = measure_z_with_correction(index=4, s=s, queries=queries)
    s, queries = measure_z_with_correction(index=7, s=s, queries=queries)
    s, queries = measure_z_with_correction(index=10, s=s, queries=queries)

    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1
    
