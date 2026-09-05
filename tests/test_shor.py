"""
Unit tests for Shor's algorithm toy factorization module.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.quantum_attacks.shor import run_shor_factorization


def test_shor_factorization_15():
    res = run_shor_factorization(N=15, base_a=7)
    assert res["successful"] is True
    assert res["modulus_N"] == 15
    assert set(res["factors"]) == {3, 5}
    assert res["period_r"] == 4
    assert res["qubit_count"] > 0


def test_shor_factorization_21():
    res = run_shor_factorization(N=21, base_a=2)
    assert res["successful"] is True
    assert res["modulus_N"] == 21
    assert set(res["factors"]) == {3, 7}
    assert res["period_r"] == 6


def test_shor_factorization_35():
    res = run_shor_factorization(N=35, base_a=3)
    assert res["successful"] is True
    assert set(res["factors"]) == {5, 7}


def test_shor_even_modulus():
    res = run_shor_factorization(N=14)
    assert res["successful"] is True
    assert res["factors"] == [2, 7]
