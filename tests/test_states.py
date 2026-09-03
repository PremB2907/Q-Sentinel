"""
Unit tests for Pauli eigenstates and state fidelity.
"""

import pytest
import numpy as np
from qds_detector.states import (
    get_statevector,
    get_density_matrix,
    calculate_fidelity,
    get_expected_probabilities,
    PAULI_STATES
)


def test_pauli_states_normalization():
    """Verify all 6 Pauli eigenstates are properly normalized pure states."""
    for name, vec in PAULI_STATES.items():
        norm = np.linalg.norm(vec)
        assert pytest.approx(norm, abs=1e-6) == 1.0


def test_pauli_states_fidelity():
    """Verify self-fidelity is 1.0 and orthogonal state fidelity is 0.0."""
    sv_0 = get_statevector("|0>")
    sv_1 = get_statevector("|1>")
    sv_plus = get_statevector("|+>")
    
    assert pytest.approx(calculate_fidelity(sv_0, sv_0), abs=1e-6) == 1.0
    assert pytest.approx(calculate_fidelity(sv_0, sv_1), abs=1e-6) == 0.0
    assert pytest.approx(calculate_fidelity(sv_0, sv_plus), abs=1e-6) == 0.5


def test_expected_probabilities():
    """Verify theoretical outcome probabilities for Pauli states across bases."""
    # |0> in Z basis -> +1: 1.0
    assert get_expected_probabilities("|0>", "Z") == {"+1": 1.0, "-1": 0.0}
    # |1> in Z basis -> -1: 1.0
    assert get_expected_probabilities("|1>", "Z") == {"+1": 0.0, "-1": 1.0}
    # |+> in X basis -> +1: 1.0
    assert get_expected_probabilities("|+>", "X") == {"+1": 1.0, "-1": 0.0}
    # |+i> in Y basis -> +1: 1.0
    assert get_expected_probabilities("|+i>", "Y") == {"+1": 1.0, "-1": 0.0}
    # |0> in X basis -> equal split 0.5
    assert get_expected_probabilities("|0>", "X") == {"+1": 0.5, "-1": 0.5}
