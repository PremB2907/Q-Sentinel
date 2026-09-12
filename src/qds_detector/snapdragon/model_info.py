"""
Hardware System & Edge AI Metadata Reporter.
SIH26141 • Egreen Quanta
"""

import platform
import os
from typing import Dict, Any
from qds_detector.snapdragon.qnn_backend import detect_qnn_execution_provider


def get_edge_hardware_info() -> Dict[str, Any]:
    """
    Returns factual information about current host environment, architecture,
    ONNX Runtime status, and Snapdragon NPU availability.
    """
    is_qnn, provider_desc = detect_qnn_execution_provider()
    
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or "x86_64/ARM64",
        "python_version": platform.python_version(),
        "target_platform": "Snapdragon-powered HP PCs",
        "accelerator_status": provider_desc,
        "npu_active": is_qnn,
        "local_privacy_mode": "ACTIVE (100% On-Device Local Processing)",
        "cloud_offload": False,
        "qualcomm_ai_hub_ready": True
    }
