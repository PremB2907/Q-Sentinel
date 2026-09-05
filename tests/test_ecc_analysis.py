"""
Unit tests for ECC discrete log quantum threat analysis module.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.quantum_attacks.ecc_analysis import analyze_ecc_dlog_threat, ToyEllipticCurve


def test_toy_curve_point_addition():
    curve = ToyEllipticCurve(a=2, b=2, p=17)
    G = (5, 1)
    assert curve.is_on_curve(G) is True
    
    # 2G = G + G
    G2 = curve.add(G, G)
    assert curve.is_on_curve(G2) is True
    assert G2 != G


def test_ecc_dlog_threat_toy_p17():
    res = analyze_ecc_dlog_threat(curve_name="toy_p17", private_key_k=7)
    assert res["successful"] is True
    assert res["actual_private_key_k"] == 7
    assert res["quantum_recovered_key_k"] == 7
    assert res["qubit_count"] > 0


def test_ecc_dlog_threat_toy_p23():
    res = analyze_ecc_dlog_threat(curve_name="toy_p23", private_key_k=5)
    assert res["successful"] is True
    assert res["quantum_recovered_key_k"] == 5
