"""
ONNX Runtime & QNN Execution Provider Hierarchy Manager.
SIH26141 • Egreen Quanta
"""

from typing import Tuple, Any, List, Optional
import os


class SnapdragonRuntimeManager:
    """
    Manages ONNX Runtime session creation adhering to strict execution provider hierarchy:
    1. QNNExecutionProvider (Snapdragon NPU)
    2. DmlExecutionProvider (DirectML GPU)
    3. CPUExecutionProvider (CPU Fallback)
    """
    def __init__(self):
        self.available_providers = self._get_system_providers()

    def _get_system_providers(self) -> List[str]:
        try:
            import onnxruntime as ort
            return ort.get_available_providers()
        except Exception:
            return ["CPUExecutionProvider"]

    def select_best_provider(self) -> Tuple[List[str], str]:
        """
        Determines best available provider list and human-readable name.
        """
        if "QNNExecutionProvider" in self.available_providers:
            return ["QNNExecutionProvider", "CPUExecutionProvider"], "Snapdragon Hexagon NPU (QNN)"
        elif "DmlExecutionProvider" in self.available_providers:
            return ["DmlExecutionProvider", "CPUExecutionProvider"], "DirectML GPU"
        elif "CUDAExecutionProvider" in self.available_providers:
            return ["CUDAExecutionProvider", "CPUExecutionProvider"], "CUDA GPU"
        else:
            return ["CPUExecutionProvider"], "CPU (OpenMP Fallback)"

    def create_session(self, model_path: str) -> Tuple[Optional[Any], str]:
        """
        Creates ONNX Runtime InferenceSession with best available execution provider.
        """
        if not os.path.exists(model_path):
            return None, "Model File Missing"

        try:
            import onnxruntime as ort
            providers, provider_name = self.select_best_provider()
            session = ort.InferenceSession(model_path, providers=providers)
            actual_provider = session.get_providers()[0]
            return session, f"{provider_name} [{actual_provider}]"
        except Exception as e:
            # Fallback to CPU if provider initialization fails
            try:
                import onnxruntime as ort
                session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
                return session, "CPU (Fallback after Provider Error)"
            except Exception:
                return None, f"ONNX Runtime Load Failed ({e})"


def get_onnx_runtime_session(model_path: str) -> Tuple[Optional[Any], str]:
    """Helper function to obtain ONNX Runtime session."""
    mgr = SnapdragonRuntimeManager()
    return mgr.create_session(model_path)
