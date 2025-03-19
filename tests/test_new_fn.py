from stimrgs_v1.new_fn import *
import pytest

def test_generate_random_rgs_v3():
    key = jax.random.key(0)
    
    edges_between_row = 7
    circuit = generate_random_rgs_v3(
        key=key,
        num_rows=4,
        num_cols=3,
        edges_between_row=edges_between_row
    )

    assert type(circuit) == str
    
    # Split by newline and take first part
    h_part = circuit.split('\n')[0].replace('H ', '')
    # Split by spaces to get individual numbers
    h_numbers = h_part.split()
    # Convert to integers if needed
    h_numbers_int = [int(num) for num in h_numbers]

    # Split by newline and take the second part
    cz_part = circuit.split('\n')[1].replace('CZ ', '')
    # Split by spaces to get individual numbers
    cz_numbers = cz_part.split()
    # Convert to integers if needed
    cz_numbers_int = [int(num) for num in cz_numbers]
    
    assert len(h_numbers_int) == 12
    assert h_numbers_int == [i for i in range(12)]

    # CZ connect 2 RGS and 3 middle nodes
    assert len(cz_numbers_int) == (edges_between_row*4) + 6
    assert cz_numbers_int[-6:] == [3, 6, 4, 7, 5, 8]
    

def test_gen_all_bell_v2():
    all_bell_stabs = gen_all_bell_v2(num_rows=4, num_cols=3)

    assert len(all_bell_stabs) == 18
    for stab in all_bell_stabs:
        assert stab.count('X') == 1
        assert stab.count('Z') == 1
        assert stab.count('_') == 10

def test_simulate_rgs():
    pass
