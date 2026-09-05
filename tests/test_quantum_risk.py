"""
Unit tests for unified deterministic quantum risk engine module.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.quantum_attacks.quantum_risk import evaluate_quantum_risk, RISK_LEVEL_CRITICAL, RISK_LEVEL_LOW


def test_quantum_risk_rsa2048_critical():
    res = evaluate_quantum_risk(algorithm_name="RSA-2048", data_retention_years=10, infrastructure_lifecycle_years=10)
    assert res["risk_level"] == RISK_LEVEL_CRITICAL
    assert res["vulnerability_score_numeric"] == 1.0
    assert res["scientific_framing"]["currently_practically_breakable"] is False


def test_quantum_risk_ml_dsa_low():
    res = evaluate_quantum_risk(algorithm_name="ML-DSA-44")
    assert res["risk_level"] == RISK_LEVEL_LOW
    assert res["vulnerability_score_numeric"] == 0.0


def test_quantum_risk_qds_teleportation():
    res = evaluate_quantum_risk(algorithm_name="QDS-Teleportation")
    assert res["risk_level"] == RISK_LEVEL_LOW
    assert "Q-Sentinel" in res["action_recommendation"]
