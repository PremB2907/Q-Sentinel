"""
Qualcomm QNN Execution Provider Detector & Status Reporter.
SIH26141 • Egreen Quanta
"""

from typing import Dict, Any, Tuple


def detect_qnn_execution_provider() -> Tuple[bool, str]:
    """
    Checks if Qualcomm QNN Execution Provider (QNNExecutionProvider) is available in ONNX Runtime.
    Returns (is_available, provider_name_or_reason).
    """
    try:
        import onnxruntime as ort
        available_providers = ort.get_available_providers()
        if "QNNExecutionProvider" in available_providers:
            return True, "QNNExecutionProvider (Snapdragon Hexagon NPU)"
        elif "SNPEExecutionProvider" in available_providers:
            return True, "SNPEExecutionProvider (Snapdragon NPU)"
        elif "DmlExecutionProvider" in available_providers:
            return False, "DmlExecutionProvider (DirectML GPU)"
        else:
            return False, "CPUExecutionProvider (Fallback)"
    except Exception as e:
        return False, f"ONNX Runtime Check Error ({e})"


def get_qnn_status_info() -> Dict[str, Any]:
    """
    Returns complete status dictionary detailing Snapdragon QNN NPU readiness.
    """
    is_qnn, provider = detect_qnn_execution_provider()
    
    return {
        "qnn_available": is_qnn,
        "active_provider": provider,
        "hardware_target": "Snapdragon-powered HP PC (Hexagon NPU)",
        "quantization_support": "INT8 / FP16 QNN Graph Execution",
        "qualcomm_ai_hub_compatible": True,
        "ubuntu_dev_mode": not is_qnn,
        "notes": (
            "QNN Execution Provider active on Snapdragon hardware. "
            if is_qnn else
            "Operating under Linux/Ubuntu development mode with ONNX Runtime CPU fallback. "
            "Deploy to Snapdragon Windows platform for hardware NPU acceleration."
        )
    }
