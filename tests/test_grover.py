"""
Unit tests for Grover search analysis module.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.quantum_attacks.grover import run_grover_search_analysis


def test_grover_search_4_bits():
    res = run_grover_search_analysis(key_space_bits=4)
    assert res["search_space_size_N"] == 16
    assert res["grover_iterations"] == 3
    assert res["grover_final_success_probability"] > 0.90
    assert res["qubit_count"] == 5


def test_grover_search_8_bits():
    res = run_grover_search_analysis(key_space_bits=8)
    assert res["search_space_size_N"] == 256
    assert res["grover_iterations"] == 12
    assert res["speedup_factor"] > 10.0


def test_grover_amplitude_trace():
    res = run_grover_search_analysis(key_space_bits=6)
    trace = res["amplitude_trace"]
    assert len(trace) == res["grover_iterations"] + 1
    assert trace[0]["target_probability"] < trace[-1]["target_probability"]
