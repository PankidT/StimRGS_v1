import pytest
import stim

from stimrgs_v1.stabilizer_operations import *


@pytest.fixture()
def stim_4arms_3bells():
    s = stim.TableauSimulator()
    s.do_circuit(
        stim.Circuit(
            """
        H 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        CZ 0 5 0 6 0 7 1 4 1 6 1 7 2 4 2 5 2 7 3 4 3 5 3 6 8 13 8 14 8 15 9 12 9 14 9 15 10 12 10 13 10 15 11 12 11 13 11 14 4 8 5 9 6 10 7 11
        """
        )
    )
    return s


@pytest.fixture()
def queries_4arms_3bells():
    """Stabilizer generator for RGS 4 arms and 2 Bells pair"""
    return [
        "X____ZZZ________",  # node 0
        "_X__Z_ZZ________",  # node 1
        "__X_ZZ_Z________",  # node 2
        "___XZZZ_________",  # node 3
        "_ZZZX___Z_______",  # node 4
        "Z_ZZ_X___Z______",  # node 5
        "ZZ_Z__X___Z_____",  # node 6
        "ZZZ____X___Z____",  # node 7
        "____Z___X____ZZZ",  # node 8
        "_____Z___X__Z_ZZ",  # node 9
        "______Z___X_ZZ_Z",  # node 10
        "_______Z___XZZZ_",  # node 11
        "_________ZZZX___",  # node 12
        "________Z_ZZ_X__",  # node 13
        "________ZZ_Z__X_",  # node 14
        "________ZZZ____X",  # node 15
    ]


@pytest.fixture
def stim_4arms_2bells():
    s = stim.TableauSimulator()
    s.do_circuit(
        stim.Circuit(
            """
        H 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        CZ 0 4 0 5 1 4 1 6 2 5 2 7 3 6 3 7 8 12 8 13 9 12 9 14 10 13 10 15 11 14 11 15 4 8 5 9 6 10 7 11
            """))
    return s

@pytest.fixture
def queries_4arms_2bells():
    """Stabilizer generator for RGS 4 arms and 2 Bells pair"""
    return [
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


@pytest.fixture
def measurement_indices():
    """Fixture providing measurement indices to test."""
    return [1, 4, 7, 10]


# ------------------------------------------------------------------------------


def test_measure_z_with_correction_loop_4arms_3bells(
    stim_4arms_3bells, queries_4arms_3bells, measurement_indices
):
    """Test measure_z_with_correction using a loop approach."""
    s = stim_4arms_3bells
    queries_copy = (
        queries_4arms_3bells.copy()
    )  # Create a copy to avoid modifying the fixture

    for idx in measurement_indices:
        s, queries_copy = measure_z_with_correction(
            index=idx, s=s, queries=queries_copy
        )

    for q in queries_copy:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    for q in queries_copy:
        if len(q) != 16:
            raise ValueError(
                f"Query {q} has length {len(q)}, but should have length 16."
            )

def test_measure_z_with_correction_loop_4arms_2bells(
    stim_4arms_2bells, queries_4arms_2bells, measurement_indices
):
    """Test measure_z_with_correction using a loop approach."""
    s = stim_4arms_2bells
    queries_copy = (
        queries_4arms_2bells.copy()
    )  # Create a copy to avoid modifying the fixture

    for idx in measurement_indices:
        s, queries_copy = measure_z_with_correction(
            index=idx, s=s, queries=queries_copy
        )

    for q in queries_copy:
        assert s.peek_observable_expectation(stim.PauliString(q)) == 1

    for q in queries_copy:
        if len(q) != 16:
            raise ValueError(
                f"Query {q} has length {len(q)}, but should have length 16."
            )