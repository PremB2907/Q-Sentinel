"""
Edge Triage & Threat Prioritization Engine.
SIH26141 • Egreen Quanta
"""

from typing import Dict, Any
from qds_detector.edge_ai.schema import SecurityEvent
from qds_detector.edge_ai.classifier import get_default_classifier
from qds_detector.edge_ai.explainer import generate_evidence_explanation


def analyze_and_triage_event(event: SecurityEvent) -> Dict[str, Any]:
    """
    Executes local edge AI threat analysis on a SecurityEvent, produces grounded evidence,
    and returns a combined advisory & authoritative decision payload.
    """
    classifier = get_default_classifier()
    ai_result = classifier.predict(event)

    explanation = generate_evidence_explanation(event, ai_result)

    # Compute triage priority level
    cls_name = ai_result["classification"]
    det_dec = event.deterministic_decision

    if det_dec == "REJECT" or cls_name == "ATTACK":
        triage_level = "P1 - CRITICAL THREAT"
        action = "BLOCK TRANSMISSION & LOG INCIDENT"
    elif det_dec == "SUSPICIOUS" or cls_name == "SUSPICIOUS":
        triage_level = "P2 - ANOMALOUS AUDIT"
        action = "FLAG FOR OPERATOR AUDIT"
    else:
        triage_level = "P3 - NORMAL"
        action = "ALLOW SIGNATURE TRANSMISSION"

    return {
        "event_id": event.event_id,
        "timestamp": event.timestamp,
        "ai_analysis": {
            "classification": ai_result["classification"],
            "top_confidence": ai_result["top_confidence"],
            "confidence_scores": ai_result["confidence_scores"],
            "execution_provider": ai_result["execution_provider"],
            "inference_latency_ms": ai_result["inference_latency_ms"]
        },
        "deterministic_verification": {
            "decision": event.deterministic_decision,
            "reasons": event.deterministic_reasons,
            "fidelity": event.fidelity,
            "z_score": event.z_score,
            "p_value": event.p_value,
            "signer_valid": event.signer_valid,
            "nonce_valid": event.nonce_valid
        },
        "triage": {
            "priority": triage_level,
            "recommended_action": action,
            "privacy_mode": "LOCAL-ONLY (100% On-Device)",
            "cloud_requests_sent": 0
        },
        "evidence_explanation": explanation
    }
