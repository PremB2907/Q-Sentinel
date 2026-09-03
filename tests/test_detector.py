"""
Unit tests for deterministic Threat Detection engine (ACCEPT, SUSPICIOUS, REJECT) with Two-Tier evaluation.
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
        fidelity=1.0,
        context=ctx,
        basis="Z"
    )
    assert res.decision == "ACCEPT"
    assert res.threat_category == "NONE"


def test_detector_reject_impersonation():
    """Verify identity context mismatch yields REJECT with IMPERSONATION threat category."""
    obs_counts = {"+1": 5000, "-1": 0}
    base_probs = {"+1": 1.0, "-1": 0.0}
    ctx = SessionContext(signer_id="Eve", expected_signer_id="Alice")
    ctx.validate()
    
    res = evaluate_threat_detection(
        observed_counts=obs_counts,
        baseline_probs=base_probs,
        fidelity=1.0,
        context=ctx,
        basis="Z"
    )
    assert res.decision == "REJECT"
    assert res.threat_category == "IMPERSONATION"


def test_detector_reject_replay():
    """Verify freshness failure yields REJECT with REPLAY threat category."""
    obs_counts = {"+1": 5000, "-1": 0}
    base_probs = {"+1": 1.0, "-1": 0.0}
    ctx = SessionContext(freshness_valid=False)
    
    res = evaluate_threat_detection(
        observed_counts=obs_counts,
        baseline_probs=base_probs,
        fidelity=1.0,
        context=ctx,
        basis="Z"
    )
    assert res.decision == "REJECT"
    assert res.threat_category == "REPLAY"


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
        context=ctx,
        basis="Z"
    )
    assert res.decision == "REJECT"
    assert res.threat_category in ["FORGERY", "CHANNEL_MANIPULATION"]
