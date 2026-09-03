"""
Configuration Dataclasses and Calibration Constants for QDS Threat Detection.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ThresholdConfig:
    """Deterministic Threshold Configuration for Threat Detector."""
    shots: int = 5000
    alpha: float = 0.01  # Significance level for statistical hypothesis testing
    min_fidelity_accept: float = 0.98
    min_fidelity_suspicious: float = 0.90
    max_probability_deviation_accept: float = 0.03
    max_probability_deviation_suspicious: float = 0.10
    
    # Protocol-layer verification flags
    require_unique_session: bool = True
    require_fresh_nonce: bool = True
    strict_context_match: bool = True


@dataclass
class SessionContext:
    """Protocol Context for Identity and Freshness Verification."""
    session_id: str = "SESS-2026-001"
    signer_id: str = "Alice_PubKey_0x8F4A"
    expected_signer_id: str = "Alice_PubKey_0x8F4A"
    nonce: str = "NONCE-987654321"
    timestamp: float = 1756900000.0
    freshness_valid: bool = True
    identity_valid: bool = True

    def validate(self) -> None:
        """Evaluate identity and freshness context validity."""
        self.identity_valid = (self.signer_id == self.expected_signer_id)


@dataclass
class ExperimentConfig:
    """Configuration for running a QDS Teleportation Experiment."""
    input_state: str = "|0>"  # Choice of |0>, |1>, |+>, |->, |+i>, |-i>
    measurement_basis: str = "Z"  # Choice of Z, X, Y
    shots: int = 5000
    seed: Optional[int] = 42
    attack_type: str = "none"  # "none", "forgery", "channel_bit_flip", "channel_phase_flip", "channel_depolarizing", "replay", "impersonation"
    attack_severity: float = 0.0  # Severity lambda in [0, 1]
    noise_model: str = "none"  # Optional simulator physical noise
    session_context: SessionContext = field(default_factory=SessionContext)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)
