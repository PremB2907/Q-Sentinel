"""
Unit tests for Pauli projective measurement operators.
"""

import pytest
from qds_detector.states import get_statevector
from qds_detector.measurements import evaluate_state_projective_probabilities, get_projectors


def test_projectors_completeness():
    """Verify P+ + P- = I for all bases."""
    for b in ["X", "Y", "Z"]:
        P_plus, P_minus = get_projectors(b)
        sum_p = P_plus + P_minus
        assert pytest.approx(sum_p[0, 0].real) == 1.0
        assert pytest.approx(sum_p[1, 1].real) == 1.0
        assert pytest.approx(sum_p[0, 1].real) == 0.0
        assert pytest.approx(sum_p[1, 0].real) == 0.0


def test_projective_probabilities_exact():
    """Verify trace probabilities for pure states."""
    sv_0 = get_statevector("|0>")
    probs_z = evaluate_state_projective_probabilities(sv_0, "Z")
    assert pytest.approx(probs_z["+1"]) == 1.0
    assert pytest.approx(probs_z["-1"]) == 0.0
    
    sv_plus = get_statevector("|+>")
    probs_x = evaluate_state_projective_probabilities(sv_plus, "X")
    assert pytest.approx(probs_x["+1"]) == 1.0
    assert pytest.approx(probs_x["-1"]) == 0.0
    
    sv_plus_i = get_statevector("|+i>")
    probs_y = evaluate_state_projective_probabilities(sv_plus_i, "Y")
    assert pytest.approx(probs_y["+1"]) == 1.0
    assert pytest.approx(probs_y["-1"]) == 0.0
