"""
Unit tests for CRQC resource estimator module.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.quantum_attacks.resource_estimator import estimate_crqc_resources


def test_estimate_crqc_resources_rsa2048():
    res = estimate_crqc_resources("RSA-2048")
    assert res["logical_qubits"] == 4098  # 2*2048 + 2
    assert res["t_gate_count"] > 1e11
    assert res["total_estimated_physical_qubits"] > 1e6
    assert res["estimated_execution_time_hours"] > 0


def test_estimate_crqc_resources_ecdsa256():
    res = estimate_crqc_resources("ECDSA-P256")
    assert res["logical_qubits"] == 2312  # 9*256 + 8
    assert res["total_estimated_physical_qubits"] > 1e5
