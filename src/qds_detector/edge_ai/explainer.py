"""
Grounded Explanation Engine for Q-Sentinel Edge Evidence.
SIH26141 • Egreen Quanta

Generates natural language evidence explanations grounded strictly in deterministic
quantum statistical telemetry (zero generative LLM hallucination).
"""

from typing import Dict, Any
from qds_detector.edge_ai.schema import SecurityEvent


def generate_evidence_explanation(event: SecurityEvent, ai_result: Dict[str, Any]) -> str:
    """
    Constructs a grounded, non-hallucinating evidence explanation text combining
    AI classification advisory confidence and authoritative deterministic verification.
    """
    cls_name = ai_result.get("classification", "UNKNOWN")
    top_conf = ai_result.get("top_confidence", 0.0) * 100.0
    provider = ai_result.get("execution_provider", "CPU")
    lat = ai_result.get("inference_latency_ms", 0.0)

    det_dec = event.deterministic_decision
    reasons = event.deterministic_reasons

    explanation_lines = [
        f"• Local Edge AI Classification: {cls_name} ({top_conf:.1f}% confidence, evaluated via {provider} in {lat:.2f} ms).",
        f"• Authoritative Security Decision: {det_dec}."
    ]

    # Grounding evidence points
    evidence_points = []
    if event.replayed_nonce:
        evidence_points.append("Nonce freshness failure (session transcript replayed)")
    if event.impersonation_flag:
        evidence_points.append("Signer identity mismatch (unauthorized key context)")
    if event.z_score > 2.58:
        evidence_points.append(f"Binomial z-score ({event.z_score:.2f}) exceeded significance bound")
    if event.fidelity < 0.98:
        evidence_points.append(f"Quantum state fidelity ({event.fidelity:.4f}) dropped below acceptance bound (0.98)")
    if event.probability_deviation > 0.03:
        evidence_points.append(f"Observed probability deviation ({event.probability_deviation:.4f}) exceeded max threshold")

    if evidence_points:
        explanation_lines.append("• Grounded Telemetry Indicators: " + "; ".join(evidence_points) + ".")
    elif reasons:
        explanation_lines.append("• Deterministic Reasons: " + "; ".join(reasons) + ".")
    else:
        explanation_lines.append("• Grounded Telemetry Indicators: Teleportation quantum state measurements strictly match theoretical Pauli eigenstate probabilities.")

    return "\n".join(explanation_lines)
