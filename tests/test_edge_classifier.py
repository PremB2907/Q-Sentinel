"""
Unit tests for Edge Threat Classifier & Explainer Engine.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.edge_ai.schema import SecurityEvent
from qds_detector.edge_ai.classifier import get_default_classifier
from qds_detector.edge_ai.explainer import generate_evidence_explanation
from qds_detector.edge_ai.triage import analyze_and_triage_event


def test_edge_classifier_prediction():
    classifier = get_default_classifier()
    evt = SecurityEvent(
        attack_type="clean",
        fidelity=1.0,
        z_score=0.1,
        p_value=0.95,
        signer_valid=True,
        nonce_valid=True
    )
    res = classifier.predict(evt)

    assert "classification" in res
    assert res["classification"] in ["NORMAL", "SUSPICIOUS", "ATTACK"]
    assert "confidence_scores" in res
    assert res["inference_latency_ms"] >= 0.0


def test_grounded_explanation_generation():
    evt = SecurityEvent(
        attack_type="replay",
        replayed_nonce=True,
        nonce_valid=False,
        z_score=3.85,
        fidelity=0.81,
        deterministic_decision="REJECT"
    )
    classifier = get_default_classifier()
    ai_res = classifier.predict(evt)

    exp_text = generate_evidence_explanation(evt, ai_res)
    assert "Local Edge AI Classification" in exp_text
    assert "Authoritative Security Decision: REJECT" in exp_text
    assert "Nonce freshness failure" in exp_text


def test_triage_analysis():
    evt = SecurityEvent(
        attack_type="impersonation",
        impersonation_flag=True,
        signer_valid=False,
        deterministic_decision="REJECT"
    )
    payload = analyze_and_triage_event(evt)
    assert payload["triage"]["priority"] == "P1 - CRITICAL THREAT"
    assert payload["triage"]["privacy_mode"] == "LOCAL-ONLY (100% On-Device)"
    assert payload["triage"]["cloud_requests_sent"] == 0
