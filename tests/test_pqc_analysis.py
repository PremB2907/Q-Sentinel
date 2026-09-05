"""
Unit tests for NIST PQC signature analysis module.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.quantum_attacks.pqc_analysis import get_pqc_scheme_metadata, list_pqc_schemes


def test_list_pqc_schemes():
    schemes = list_pqc_schemes()
    assert "ML-DSA-44" in schemes
    assert "SLH-DSA-128f" in schemes


def test_pqc_scheme_metadata_ml_dsa():
    meta = get_pqc_scheme_metadata("ML-DSA-44")
    assert meta["family"] == "Module-Lattice (Dilithium)"
    assert meta["public_key_bytes"] == 1312
    assert meta["signature_bytes"] == 2420
    assert meta["pubkey_overhead_vs_ecdsa"] > 1.0


def test_pqc_scheme_metadata_slh_dsa():
    meta = get_pqc_scheme_metadata("SLH-DSA-128f")
    assert meta["family"] == "Stateless Hash-Based (SPHINCS+)"
    assert meta["signature_bytes"] == 17088
