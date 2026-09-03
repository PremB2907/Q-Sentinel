"""
Deterministic Rule-Based QDS Threat Detector.

Evaluates quantum measurement distributions, state fidelity, and protocol layer context
to classify signature verification requests as ACCEPT, SUSPICIOUS, or REJECT.
Strictly contains NO AI/ML models.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Tuple
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
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision,
            "reason": self.reason,
            "evidence": self.evidence
        }


def evaluate_threat_detection(
    observed_counts: Dict[str, int],
    baseline_probs: Dict[str, float],
    fidelity: float,
    context: SessionContext,
    thresholds: ThresholdConfig = ThresholdConfig()
) -> DetectionResult:
    """
    Deterministic Threat Detection Decision Algorithm.
    
    Order of Evaluation:
    1. Check protocol identity context (Impersonation check)
    2. Check protocol freshness / nonce context (Replay check)
    3. Compute probability deviation, z-score, p-value, chi2
    4. Apply calibrated deterministic thresholds to render ACCEPT / SUSPICIOUS / REJECT.
    """
    shots = sum(observed_counts.values())
    observed_probs = {k: v / shots for k, v in observed_counts.items()}
    
    # Compute statistical evidence metrics
    deviation = compute_probability_deviation(observed_probs, baseline_probs)
    z_score, p_value, se = compute_z_score_and_p_value(observed_counts, baseline_probs, shots)
    chi2, chi2_p_val = compute_chi_square_test(observed_counts, baseline_probs, shots)
    conf_intervals = compute_confidence_intervals(observed_counts, shots, confidence_level=1.0 - thresholds.alpha)
    
    evidence = {
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
        "confidence_intervals": conf_intervals,
        "identity_valid": context.identity_valid,
        "freshness_valid": context.freshness_valid,
        "signer_id": context.signer_id,
        "expected_signer_id": context.expected_signer_id,
        "session_id": context.session_id,
        "nonce": context.nonce
    }

    # 1. Identity Check
    if not context.identity_valid:
        return DetectionResult(
            decision="REJECT",
            reason="IMPERSONATION_ATTACK: Signer identity context mismatch.",
            evidence=evidence
        )

    # 2. Freshness Check
    if not context.freshness_valid:
        return DetectionResult(
            decision="REJECT",
            reason="REPLAY_ATTACK: Stale transcript / nonce reuse detected.",
            evidence=evidence
        )

    # 3. Deterministic Statistical & Fidelity Rule Evaluation
    is_accept_deviation = (deviation <= thresholds.max_probability_deviation_accept)
    is_accept_p_val = (p_value >= thresholds.alpha)
    is_accept_fidelity = (fidelity >= thresholds.min_fidelity_accept)
    
    is_suspicious_deviation = (deviation <= thresholds.max_probability_deviation_suspicious)
    is_suspicious_fidelity = (fidelity >= thresholds.min_fidelity_suspicious)

    # Rule: ACCEPT
    if is_accept_deviation and is_accept_p_val and is_accept_fidelity:
        return DetectionResult(
            decision="ACCEPT",
            reason="LEGITIMATE_SIGNATURE: Statistical outcome compatible with baseline within calibrated confidence bounds.",
            evidence=evidence
        )

    # Rule: SUSPICIOUS
    if is_suspicious_deviation and is_suspicious_fidelity:
        return DetectionResult(
            decision="SUSPICIOUS",
            reason="STATISTICAL_ANOMALY: Measurement deviation or fidelity reduction near acceptance threshold.",
            evidence=evidence
        )

    # Rule: REJECT
    reject_reasons = []
    if deviation > thresholds.max_probability_deviation_suspicious:
        reject_reasons.append(f"High statistical outcome deviation ({deviation:.3f} > {thresholds.max_probability_deviation_suspicious:.3f})")
    if p_value < thresholds.alpha:
        reject_reasons.append(f"Statistically significant distribution shift (p-value {p_value:.4e} < {thresholds.alpha:.2f})")
    if fidelity < thresholds.min_fidelity_suspicious:
        reject_reasons.append(f"Low state fidelity ({fidelity:.3f} < {thresholds.min_fidelity_suspicious:.3f})")
        
    reason_str = "REJECT: " + " | ".join(reject_reasons) if reject_reasons else "REJECT: Quantum statistical deviation exceeded calibrated thresholds."
    
    return DetectionResult(
        decision="REJECT",
        reason=reason_str,
        evidence=evidence
    )
