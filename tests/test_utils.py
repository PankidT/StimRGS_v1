from dataclasses import dataclass
import stim


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

def test_stim_rgs_3arms(s: stim.TableauSimulator) -> None:
    """
    For checking if the stim tableausimulator have the correct stabilizer form
    """
    # Checking number of nodes
    assert len(s.current_inverse_tableau()) == 12

    # Check stabilizer generator
    
