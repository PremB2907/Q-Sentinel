"""
Deterministic Rule-Based QDS Threat Detector with Two-Tier Architecture.

Tier 1: Protocol-Layer Context (Identity Match & Nonce Freshness)
Tier 2: Quantum-Layer Verification (Basis-specific empirical thresholds, z-score, chi-square, fidelity)

Strictly contains NO AI/ML models.
"""

from dataclasses import dataclass, field
from typing import Dict, Any
import numpy as np

from qds_detector.config import ThresholdConfig, SessionContext
from qds_detector.statistics import (
    compute_probability_deviation,
    compute_z_score_and_p_value,
    compute_chi_square_test,
    compute_confidence_intervals
)


@dataclass
class DetectionResult:
    """Output structure of Threat Detection Decision Engine."""
    decision: str  # "ACCEPT", "SUSPICIOUS", "REJECT"
    reason: str  # Description of decision rationale
    threat_category: str = "NONE"  # "NONE", "IMPERSONATION", "REPLAY", "FORGERY", "CHANNEL_MANIPULATION"
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision,
            "reason": self.reason,
            "threat_category": self.threat_category,
            "evidence": self.evidence
        }


def evaluate_threat_detection(
    observed_counts: Dict[str, int],
    baseline_probs: Dict[str, float],
    fidelity: float,
    context: SessionContext,
    basis: str = "Z",
    thresholds: ThresholdConfig = ThresholdConfig()
) -> DetectionResult:
    """
    Two-Tier Deterministic Threat Detection Algorithm.
    
    TIER 1 (Protocol Layer):
    1. Check protocol identity context (Impersonation check)
    2. Check protocol freshness / nonce context (Replay check)
    
    TIER 2 (Quantum Layer):
    3. Compute probability deviation, z-score, p-value, chi2, confidence bounds
    4. Apply basis-specific empirical thresholds and analytical statistical limits.
    """
    shots = sum(observed_counts.values())
    observed_probs = {k: v / shots for k, v in observed_counts.items()}
    
    # Tier 2 Quantum Statistics Computation
    deviation = compute_probability_deviation(observed_probs, baseline_probs)
    z_score, p_value, se = compute_z_score_and_p_value(observed_counts, baseline_probs, shots)
    chi2, chi2_p_val = compute_chi_square_test(observed_counts, baseline_probs, shots)
    conf_intervals = compute_confidence_intervals(observed_counts, shots, confidence_level=1.0 - thresholds.alpha)
    
    max_dev_accept = thresholds.get_max_deviation_accept(basis)
    min_fid_accept = thresholds.get_min_fidelity_accept(basis)
    
    tier1_evidence = {
        "identity_valid": context.identity_valid,
        "freshness_valid": context.freshness_valid,
        "signer_id": context.signer_id,
        "expected_signer_id": context.expected_signer_id,
        "session_id": context.session_id,
        "nonce": context.nonce
    }
    
    tier2_evidence = {
        "measurement_basis": basis,
        "observed_counts": observed_counts,
        "observed_probabilities": observed_probs,
        "baseline_probabilities": baseline_probs,
        "shots": shots,
        "fidelity": float(fidelity),
        "deviation": float(deviation),
        "basis_max_dev_threshold": float(max_dev_accept),
        "basis_min_fidelity_threshold": float(min_fid_accept),
        "z_score": float(z_score),
        "p_value": float(p_value),
        "chi2_statistic": float(chi2),
        "chi2_p_value": float(chi2_p_val),
        "confidence_intervals": conf_intervals
    }

    evidence = {
        "tier1_protocol": tier1_evidence,
        "tier2_quantum": tier2_evidence,
        # Flattened metrics for backward compatibility
        "observed_counts": observed_counts,
        "observed_probabilities": observed_probs,
        "baseline_probabilities": baseline_probs,
        "shots": shots,
        "fidelity": float(fidelity),
        "deviation": float(deviation),
        "z_score": float(z_score),
        "p_value": float(p_value),
        "chi2_statistic": float(chi2),
        "chi2_p_value": float(chi2_p_val),
        "identity_valid": context.identity_valid,
        "freshness_valid": context.freshness_valid
    }

    # --- TIER 1: PROTOCOL LAYER VERIFICATION ---
    if not context.identity_valid:
        return DetectionResult(
            decision="REJECT",
            reason="TIER 1 PROTOCOL FAILURE: Signer identity context mismatch.",
            threat_category="IMPERSONATION",
            evidence=evidence
        )

    if not context.freshness_valid:
        return DetectionResult(
            decision="REJECT",
            reason="TIER 1 PROTOCOL FAILURE: Stale transcript / nonce reuse detected.",
            threat_category="REPLAY",
            evidence=evidence
        )

    # --- TIER 2: QUANTUM LAYER VERIFICATION ---
    is_accept_deviation = (deviation <= max_dev_accept)
    is_accept_p_val = (p_value >= thresholds.alpha)
    is_accept_fidelity = (fidelity >= min_fid_accept)
    
    is_suspicious_deviation = (deviation <= thresholds.max_probability_deviation_suspicious)
    is_suspicious_fidelity = (fidelity >= thresholds.min_fidelity_suspicious)

    # Rule: ACCEPT
    if is_accept_deviation and is_accept_p_val and is_accept_fidelity:
        return DetectionResult(
            decision="ACCEPT",
            reason="LEGITIMATE SIGNATURE: Quantum measurement statistics match calibrated basis threshold.",
            threat_category="NONE",
            evidence=evidence
        )

    # Rule: SUSPICIOUS
    if is_suspicious_deviation and is_suspicious_fidelity:
        return DetectionResult(
            decision="SUSPICIOUS",
            reason="STATISTICAL ANOMALY: Measurement outcome near acceptance threshold bounds.",
            threat_category="QUANTUM_ANOMALY",
            evidence=evidence
        )

    # Rule: REJECT
    reject_reasons = []
    category = "FORGERY"
    
    if deviation > thresholds.max_probability_deviation_suspicious:
        reject_reasons.append(f"Basis {basis} deviation ({deviation:.3f} > {max_dev_accept:.3f})")
    if p_value < thresholds.alpha:
        reject_reasons.append(f"Significant distribution shift (p-value {p_value:.4e} < {thresholds.alpha:.2f})")
    if fidelity < thresholds.min_fidelity_suspicious:
        reject_reasons.append(f"Low fidelity ({fidelity:.3f} < {min_fid_accept:.3f})")
        category = "CHANNEL_MANIPULATION"
        
    reason_str = "TIER 2 QUANTUM FAILURE: " + " | ".join(reject_reasons)
    
    return DetectionResult(
        decision="REJECT",
        reason=reason_str,
        threat_category=category,
        evidence=evidence
    )
