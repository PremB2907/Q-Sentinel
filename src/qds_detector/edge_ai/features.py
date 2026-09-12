"""
Feature Extractor Pipeline for Edge Security Events.
SIH26141 • Egreen Quanta
"""

import numpy as np
from typing import List, Dict, Any
from qds_detector.edge_ai.schema import SecurityEvent


FEATURE_NAMES = [
    "fidelity",
    "probability_deviation",
    "z_score",
    "p_value",
    "chi2_statistic",
    "attack_severity",
    "signer_valid",
    "nonce_valid",
    "session_valid",
    "replayed_nonce",
    "impersonation_flag",
    "shots_normalized"
]


def extract_feature_vector(event: SecurityEvent) -> np.ndarray:
    """
    Converts a SecurityEvent dataclass into a 1D numerical feature array (12 dimensions).
    All values are floating-point representations suitable for model inference.
    """
    shots_norm = float(event.shots) / 5000.0  # Normalize to [0, 1] range based on max shots
    
    vec = np.array([
        float(event.fidelity),
        float(event.probability_deviation),
        float(event.z_score),
        float(event.p_value),
        float(event.chi2_statistic),
        float(event.attack_severity),
        1.0 if event.signer_valid else 0.0,
        1.0 if event.nonce_valid else 0.0,
        1.0 if event.session_valid else 0.0,
        1.0 if event.replayed_nonce else 0.0,
        1.0 if event.impersonation_flag else 0.0,
        float(shots_norm)
    ], dtype=np.float32)
    
    return vec


def extract_batch_features(events: List[SecurityEvent]) -> np.ndarray:
    """Extract 2D matrix (N, 12) from list of SecurityEvent instances."""
    if not events:
        return np.empty((0, len(FEATURE_NAMES)), dtype=np.float32)
    return np.vstack([extract_feature_vector(e) for e in events])
