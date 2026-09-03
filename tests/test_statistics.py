"""
Unit tests for statistical evaluation utilities (z-score, chi-square, confidence bounds).
"""

import pytest
from qds_detector.statistics import (
    compute_probability_deviation,
    compute_z_score_and_p_value,
    compute_chi_square_test,
    compute_confidence_intervals
)


def test_probability_deviation():
    """Verify maximum probability deviation calculation."""
    obs = {"+1": 0.8, "-1": 0.2}
    base = {"+1": 1.0, "-1": 0.0}
    dev = compute_probability_deviation(obs, base)
    assert pytest.approx(dev, abs=1e-6) == 0.2


def test_z_score_clean():
    """Verify z-score for matching distribution is near 0 with large p-value (~1.0)."""
    obs_counts = {"+1": 5000, "-1": 0}
    base_probs = {"+1": 1.0, "-1": 0.0}
    z, p_val, se = compute_z_score_and_p_value(obs_counts, base_probs, shots=5000)
    assert pytest.approx(z, abs=0.1) == 0.0
    assert p_val >= 0.90


def test_z_score_forgery_shift():
    """Verify z-score for shifted distribution produces tiny p-value (< 0.001)."""
    obs_counts = {"+1": 4000, "-1": 1000}
    base_probs = {"+1": 1.0, "-1": 0.0}
    z, p_val, se = compute_z_score_and_p_value(obs_counts, base_probs, shots=5000)
    assert p_val < 1e-4
