"""
Unit tests for 3-qubit quantum teleportation circuit execution across all 6 Pauli eigenstates.
"""

import pytest
from qds_detector.teleportation import run_teleportation_experiment


@pytest.mark.parametrize("state_name, basis, expected_outcome", [
    ("|0>", "Z", "+1"),
    ("|1>", "Z", "-1"),
    ("|+>", "X", "+1"),
    ("|->", "X", "-1"),
    ("|+i>", "Y", "+1"),
    ("|-i>", "Y", "-1"),
])
def test_clean_teleportation_pauli_eigenstates(state_name, basis, expected_outcome):
    """
    Verify clean teleportation succeeds for all six Pauli eigenstates:
    The receiver outcome matching the input state eigen-value should be near 1.0 (prob >= 0.98).
    """
    res = run_teleportation_experiment(
        input_state=state_name,
        measurement_basis=basis,
        shots=5000,
        seed=42
    )
    
    obs_probs = res["observed_probabilities"]
    assert obs_probs[expected_outcome] >= 0.98
    
    # Verify all 4 Bell measurement combinations (00, 01, 10, 11) occurred with ~25% probability
    bell_counts = res["bell_counts"]
    for b_bits, count in bell_counts.items():
        prob = count / 5000
        assert pytest.approx(prob, abs=0.05) == 0.25
