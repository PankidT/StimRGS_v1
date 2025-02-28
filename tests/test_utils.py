from dataclasses import dataclass
from src.stimrgs_v1.utils import stim_rgs_3arms
import stim
import pytest

@dataclass
class RGS_3arms:
    """ Contain RGS 3 arms information """
    queries =  [
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

def test_stim_rgs_3arms() -> None:
    """
    For checking if the stim tableausimulator have the correct stabilizer form
    """
    s = stim_rgs_3arms()
    # Checking number of nodes
    assert len(s.current_inverse_tableau()) == 12

    # Check stabilizer generator
    queries = RGS_3arms().queries
    for q in queries:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

def test_mesure_z_with_correction() -> None:
    pass

def test_is_subset() -> None:
    pass

def test_generate_combinations_with_adjustable_replacement() -> None:
    pass
