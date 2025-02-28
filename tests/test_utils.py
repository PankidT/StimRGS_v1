from stimrgs_v1.utils import *

def test_is_subset() -> None:
    assert is_subset([1, 2, 3], [1, 2, 3, 4, 5])
    assert not is_subset([1, 2, 3], [2, 3, 4, 5, 6])
    assert is_subset([], [1, 2, 3])
    assert is_subset([1, 2], [1, 2])

def test_generate_combinations_with_adjustable_replacement() -> None:
    pass
