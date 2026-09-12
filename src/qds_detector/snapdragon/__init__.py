"""
Snapdragon Hardware & Execution Provider Abstraction Package.
"""

from qds_detector.snapdragon.runtime import SnapdragonRuntimeManager, get_onnx_runtime_session
from qds_detector.snapdragon.qnn_backend import detect_qnn_execution_provider, get_qnn_status_info
from qds_detector.snapdragon.model_info import get_edge_hardware_info
from qds_detector.snapdragon.benchmark import run_edge_benchmark

__all__ = [
    "SnapdragonRuntimeManager",
    "get_onnx_runtime_session",
    "detect_qnn_execution_provider",
    "get_qnn_status_info",
    "get_edge_hardware_info",
    "run_edge_benchmark",
]
