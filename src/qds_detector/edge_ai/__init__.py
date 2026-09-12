"""
Edge AI Intelligence Layer for Q-Sentinel Edge.
Provides typed security event schemas, feature extraction, local ONNX inference,
explainer grounding, and triage functions.
"""

from qds_detector.edge_ai.schema import SecurityEvent
from qds_detector.edge_ai.features import extract_feature_vector, FEATURE_NAMES

__all__ = [
    "SecurityEvent",
    "extract_feature_vector",
    "FEATURE_NAMES",
]
