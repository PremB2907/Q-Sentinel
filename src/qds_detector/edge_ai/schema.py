"""
Standard Typed Security Event Schema for Q-Sentinel Edge Telemetry.
SIH26141 • Egreen Quanta
"""

import time
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional


@dataclass
class SecurityEvent:
    """
    Typed Security Event representing single Q-Sentinel telemetry record.
    Consolidated from quantum measurement physics and protocol integrity context.
    """
    event_id: str = field(default_factory=lambda: f"EVT-{int(time.time()*1000)}")
    timestamp: float = field(default_factory=time.time)
    input_state: str = "|0>"
    measurement_basis: str = "Z"
    shots: int = 1000
    attack_type: str = "clean"  # "clean", "state_forgery", "bit_flip", "phase_flip", "depolarizing", "replay", "impersonation"
    attack_severity: float = 0.0
    fidelity: float = 1.0
    probability_deviation: float = 0.0
    z_score: float = 0.0
    p_value: float = 1.0
    chi2_statistic: float = 0.0
    signer_valid: bool = True
    nonce_valid: bool = True
    session_valid: bool = True
    replayed_nonce: bool = False
    impersonation_flag: bool = False
    deterministic_decision: str = "ACCEPT"  # "ACCEPT", "SUSPICIOUS", "REJECT"
    deterministic_reasons: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize dataclass instance to standard dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityEvent":
        """Construct SecurityEvent from dictionary payload safely."""
        known_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered)

    @classmethod
    def from_experiment_record(cls, record: Dict[str, Any]) -> "SecurityEvent":
        """Convert standard Q-Sentinel experiment record dictionary into SecurityEvent."""
        reason_str = record.get("reason", "")
        reasons = [r.strip() for r in reason_str.split(";") if r.strip()] if reason_str else []
        
        attack = record.get("attack", "none")
        if attack == "none":
            attack = "clean"

        return cls(
            event_id=record.get("experiment_id", f"EVT-{int(time.time()*1000)}"),
            timestamp=time.time(),
            input_state=record.get("input_state", "|0>"),
            measurement_basis=record.get("measurement_basis", "Z"),
            shots=int(record.get("shots", 1000)),
            attack_type=attack,
            attack_severity=float(record.get("attack_severity", 0.0)),
            fidelity=float(record.get("fidelity", 1.0)),
            probability_deviation=float(record.get("deviation", 0.0)),
            z_score=float(record.get("z_score", 0.0)),
            p_value=float(record.get("p_value", 1.0)),
            chi2_statistic=float(record.get("chi2_statistic", 0.0)),
            signer_valid=bool(record.get("identity_valid", True)),
            nonce_valid=bool(record.get("freshness_valid", True)),
            session_valid=bool(record.get("identity_valid", True) and record.get("freshness_valid", True)),
            replayed_nonce=not bool(record.get("freshness_valid", True)),
            impersonation_flag=not bool(record.get("identity_valid", True)),
            deterministic_decision=record.get("decision", "ACCEPT"),
            deterministic_reasons=reasons
        )
