from stimrgs_v1.utils import *

def test_is_subset() -> None:
    assert is_subset([1, 2, 3], [1, 2, 3, 4, 5])
    assert not is_subset([1, 2, 3], [2, 3, 4, 5, 6])
    assert is_subset([], [1, 2, 3])
    assert is_subset([1, 2], [1, 2])

def test_generate_combinations_with_adjustable_replacement() -> None:
    pass

def test_find_neighbors_from_stim_tableau() -> None:
    queries = [
        "XZZZ_",
        "ZX___",
        "Z_XZZ",
        "Z_ZX_",
        "__Z_X"
    ]
    for index in range(len(queries)):
        neighbors = find_neighbors_from_stim_tableau(index=index, queries=queries)

        # Check if the number of neighbors is correct
        assert len(neighbors) == queries[index].count('Z')

        # Check if the neighbors are correct
        if index == 0:
            assert neighbors == [1, 2, 3]
        elif index == 1:
            assert neighbors == [0]
        elif index == 2:
            assert neighbors == [0, 3, 4]
        elif index == 3:
            assert neighbors == [0, 2]
        elif index == 4:
            assert neighbors == [2]

def test_has_edge() -> None:
    test_cases = [
        ((0, 1), True),   # Node 0 should be connected to node 1        
        ((1, 2), True),  # Node 1 should not be connected to node 2
        ((2, 3), True),   # Node 1 should be connected to node 3
        ((0, 2), False),  # Node 0 should not be connected to node 2
        ((1, 3), False),  # Node 1 should not be connected to node 3
        ((0, 3), False),  # Node 0 should not be connected to node 3
        ((2, 0), False),  # Node 2 should not be connected to node 0
    ]

    sample_stabilizers = [
        "XZ__",
        "ZXZ_",
        "_ZXZ",
        "__ZX" 
    ]

    for (n1, n2), expected in test_cases:
        result = has_edge(n1, n2, sample_stabilizers)
        if result == expected:
            # print(f"PASS: Edge between {n1} and {n2} is {'present' if expected else 'absent'} as expected")
            continue
        else:
            # print(f"FAIL: Edge between {n1} and {n2} should be {'present' if expected else 'absent'} but got {'present' if result else 'absent'}") 
            assert False

def test_find_neighbors_from_selected_node():
    test_cases = [0, 1, 1, 2, 2, 3, 3, 4]
    for i in range(5):
        if i == 0:
            assert find_neighbors_from_selected_node(test_cases, i) == [1]
        elif i == 1:
            assert find_neighbors_from_selected_node(test_cases, i) == [0, 2]
        elif i == 2:
            assert find_neighbors_from_selected_node(test_cases, i) == [1, 3]
        elif i == 3:
            assert find_neighbors_from_selected_node(test_cases, i) == [2, 4]
        elif i == 4:
            assert find_neighbors_from_selected_node(test_cases, i) == [3]

def test_extract_numbers_after_cz():
    circuit = '''
        H 0 1 2 3 4
        CZ 0 1 1 2 2 3 3 4
    '''
    result = extract_numbers_after_cz(circuit)
    assert result == [0, 1, 1, 2, 2, 3, 3, 4]
    

def test_filter_groups():
    group = [0, 1, 1, 2, 2, 3, 3, 4]
    filter_test = [(0, 1), (1, 3), (1, 4)]
    assert filter_groups(group, filter_test) == [1, 2, 1, 3, 1, 4, 2, 3, 3, 4]    

def generate_h_cz_string():
    pass

def test_local_complementation_stim() -> None:
    queries = [
        "XZ___",
        "ZXZ__", 
        "_ZXZ_", 
        "__ZXZ", 
        "___ZX"        
    ]
    circuit = """
        H 0 1 2 3 4
        CZ 0 1 1 2 2 3 3 4
    """

    for idx in range(len(queries)):
        s, queries, circuit = local_complementation_stim(index=idx, queries=queries, circuit=circuit)         

        if idx == 0:
            assert queries[0] == "XZ___"
            assert queries[1] == "ZXZ__"
            assert queries[2] == "_ZXZ_"
            assert queries[3] == "__ZXZ"
            assert queries[4] == "___ZX"
            assert circuit == """H 0 1 2 3 4\nCZ 0 1 1 2 2 3 3 4"""
            for q in queries:
                assert s.peek_observable_expectation(stim.PauliString(q)) == 1

        elif idx == 1:
            assert queries[0] == "XZZ__"
            assert queries[1] == "ZXZ__"
            assert queries[2] == "ZZXZ_"
            assert queries[3] == "__ZXZ"
            assert queries[4] == "___ZX"
            assert circuit == """H 0 1 2 3 4\nCZ 0 1 0 2 1 2 2 3 3 4"""
            for q in queries:
                assert s.peek_observable_expectation(stim.PauliString(q)) == 1

        elif idx == 2:
            assert queries[0] == "X_ZZ_"
            assert queries[1] == "_XZZ_"
            assert queries[2] == "ZZXZ_"
            assert queries[3] == "ZZZXZ"
            assert queries[4] == "___ZX"
            print(circuit)
            assert circuit == """H 0 1 2 3 4\nCZ 0 2 0 3 1 2 1 3 2 3 3 4"""
            for q in queries:
                assert s.peek_observable_expectation(stim.PauliString(q)) == 1

        elif idx == 3:
            assert queries[0] == "XZ_ZZ"
            assert queries[1] == "ZX_ZZ"
            assert queries[2] == "__XZZ"
            assert queries[3] == "ZZZXZ"
            assert queries[4] == "ZZZZX" 
            assert circuit == """H 0 1 2 3 4\nCZ 0 1 0 3 0 4 1 3 1 4 2 3 2 4 3 4"""
            for q in queries:
                assert s.peek_observable_expectation(stim.PauliString(q)) == 1

        elif idx == 4:
            assert queries[0] == "X_Z_Z"
            assert queries[1] == "_XZ_Z"
            assert queries[2] == "ZZX_Z"
            assert queries[3] == "___XZ"
            assert queries[4] == "ZZZZX"
            assert circuit == """H 0 1 2 3 4\nCZ 0 2 0 4 1 2 1 4 2 4 3 4"""
            for q in queries:
                assert s.peek_observable_expectation(stim.PauliString(q)) == 1