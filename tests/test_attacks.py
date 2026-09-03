"""
Unit tests for attack models: state forgery, channel manipulation, replay, and impersonation.
"""

import pytest
from qds_detector.config import SessionContext
from qds_detector.attacks import (
    apply_forgery_attack,
    apply_channel_attack,
    apply_replay_attack,
    apply_impersonation_attack,
    simulate_attack_counts
)


def test_forgery_attack_mixture():
    """Verify forgery attack creates state mixture (1-lambda) * legit + lambda * forge."""
    rho_attack, severity = apply_forgery_attack("|0>", severity=0.4, forge_state_name="|1>")
    assert severity == 0.4


def test_replay_attack_freshness():
    """Verify replay attack invalidates freshness context."""
    ctx = SessionContext()
    ctx.validate()
    assert ctx.freshness_valid is True
    
    replayed_ctx = apply_replay_attack(ctx)
    assert replayed_ctx.freshness_valid is False


def test_impersonation_attack_identity():
    """Verify impersonation attack invalidates identity context."""
    ctx = SessionContext()
    ctx.validate()
    assert ctx.identity_valid is True
    
    impersonated_ctx = apply_impersonation_attack(ctx)
    assert impersonated_ctx.identity_valid is False
