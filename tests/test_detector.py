"""
Unit tests for deterministic Threat Detection engine (ACCEPT, SUSPICIOUS, REJECT).
"""

import pytest
from qds_detector.config import ThresholdConfig, SessionContext
from qds_detector.detector import evaluate_threat_detection


def test_detector_accept_clean():
    """Verify clean run with matching distribution and high fidelity yields ACCEPT."""
    obs_counts = {"+1": 5000, "-1": 0}
    base_probs = {"+1": 1.0, "-1": 0.0}
    ctx = SessionContext()
    ctx.validate()
    
    res = evaluate_threat_detection(
        observed_counts=obs_counts,
        baseline_probs=base_probs,
        fidelity=0.999,
        context=ctx
    )
    assert res.decision == "ACCEPT"


def test_detector_reject_impersonation():
    """Verify identity context mismatch yields REJECT with IMPERSONATION_ATTACK reason."""
    obs_counts = {"+1": 5000, "-1": 0}
    base_probs = {"+1": 1.0, "-1": 0.0}
    ctx = SessionContext(signer_id="Eve", expected_signer_id="Alice")
    ctx.validate()
    
    res = evaluate_threat_detection(
        observed_counts=obs_counts,
        baseline_probs=base_probs,
        fidelity=1.0,
        context=ctx
    )
    assert res.decision == "REJECT"
    assert "IMPERSONATION" in res.reason


def test_detector_reject_replay():
    """Verify freshness failure yields REJECT with REPLAY_ATTACK reason."""
    obs_counts = {"+1": 5000, "-1": 0}
    base_probs = {"+1": 1.0, "-1": 0.0}
    ctx = SessionContext(freshness_valid=False)
    
    res = evaluate_threat_detection(
        observed_counts=obs_counts,
        baseline_probs=base_probs,
        fidelity=1.0,
        context=ctx
    )
    assert res.decision == "REJECT"
    assert "REPLAY" in res.reason


def test_detector_reject_high_forgery():
    """Verify distribution shift from state forgery yields REJECT."""
    obs_counts = {"+1": 2500, "-1": 2500}  # 50% deviation from expected 100%
    base_probs = {"+1": 1.0, "-1": 0.0}
    ctx = SessionContext()
    ctx.validate()
    
    res = evaluate_threat_detection(
        observed_counts=obs_counts,
        baseline_probs=base_probs,
        fidelity=0.5,
        context=ctx
    )
    assert res.decision == "REJECT"
