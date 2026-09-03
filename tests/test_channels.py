"""
Unit tests for quantum noise channels.
"""

import pytest
from qds_detector.states import get_statevector
from qds_detector.measurements import evaluate_state_projective_probabilities
from qds_detector.channels import (
    apply_bit_flip_channel,
    apply_phase_flip_channel,
    apply_depolarizing_channel
)


def test_bit_flip_channel():
    """Verify bit flip channel turns |0> to |1> with probability p."""
    sv_0 = get_statevector("|0>")
    rho_noisy = apply_bit_flip_channel(sv_0, p=0.2)
    probs = evaluate_state_projective_probabilities(rho_noisy, "Z")
    
    assert pytest.approx(probs["+1"], abs=1e-5) == 0.8
    assert pytest.approx(probs["-1"], abs=1e-5) == 0.2


def test_phase_flip_channel():
    """Verify phase flip channel degrades |+> in X basis with probability p."""
    sv_plus = get_statevector("|+>")
    rho_noisy = apply_phase_flip_channel(sv_plus, p=0.3)
    probs = evaluate_state_projective_probabilities(rho_noisy, "X")
    
    assert pytest.approx(probs["+1"], abs=1e-5) == 0.7
    assert pytest.approx(probs["-1"], abs=1e-5) == 0.3


def test_depolarizing_channel():
    """Verify depolarizing channel under blueprint formula (1-p)*rho + (p/3)*(X*rho*X + Y*rho*Y + Z*rho*Z)."""
    sv_0 = get_statevector("|0>")
    rho_noisy = apply_depolarizing_channel(sv_0, p=1.0)
    probs = evaluate_state_projective_probabilities(rho_noisy, "Z")
    
    # Under blueprint formula at p=1.0: Z gives 1/3 |0><0| and X,Y give 2/3 |1><1|
    assert pytest.approx(probs["+1"], abs=0.01) == 1.0 / 3.0
    assert pytest.approx(probs["-1"], abs=0.01) == 2.0 / 3.0
