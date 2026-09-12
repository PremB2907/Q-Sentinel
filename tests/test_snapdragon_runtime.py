"""
Unit tests for Snapdragon Runtime & QNN Execution Provider Abstraction.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.snapdragon.qnn_backend import detect_qnn_execution_provider, get_qnn_status_info
from qds_detector.snapdragon.runtime import SnapdragonRuntimeManager
from qds_detector.snapdragon.model_info import get_edge_hardware_info
from qds_detector.snapdragon.benchmark import run_edge_benchmark


def test_qnn_execution_provider_detection():
    is_qnn, provider = detect_qnn_execution_provider()
    assert isinstance(is_qnn, bool)
    assert isinstance(provider, str)


def test_qnn_status_info():
    info = get_qnn_status_info()
    assert "qnn_available" in info
    assert "hardware_target" in info
    assert info["hardware_target"] == "Snapdragon-powered HP PC (Hexagon NPU)"


def test_snapdragon_runtime_manager():
    mgr = SnapdragonRuntimeManager()
    providers, name = mgr.select_best_provider()
    assert len(providers) >= 1
    assert "CPUExecutionProvider" in providers


def test_hardware_info():
    hw = get_edge_hardware_info()
    assert hw["target_platform"] == "Snapdragon-powered HP PCs"
    assert hw["cloud_offload"] is False


def test_edge_benchmark():
    bm = run_edge_benchmark(num_iterations=10, warmup_iterations=2)
    assert bm["benchmark_iterations"] == 10
    assert bm["avg_latency_ms"] >= 0.0
    assert bm["throughput_fps"] > 0.0
