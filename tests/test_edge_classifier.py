"""
Unit tests for Edge Threat Classifier, Explainer Engine & Feature Leakage Safety.
SIH26141 • Egreen Quanta
Qualcomm Snapdragon AI Lab Challenge
"""

import pytest
import numpy as np
import onnxruntime as ort
from qds_detector.edge_ai.schema import SecurityEvent
from qds_detector.edge_ai.features import extract_feature_vector, FEATURE_NAMES
from qds_detector.edge_ai.classifier import get_default_classifier, EdgeThreatClassifier
from qds_detector.edge_ai.explainer import generate_evidence_explanation
from qds_detector.edge_ai.triage import analyze_and_triage_event


def test_feature_vector_leakage_safety():
    """Assert attack_severity and attack_type are strictly excluded from feature inputs."""
    assert "attack_severity" not in FEATURE_NAMES
    assert "attack_type" not in FEATURE_NAMES
    assert len(FEATURE_NAMES) == 11

    evt = SecurityEvent(
        attack_type="state_forgery",
        attack_severity=0.75,
        fidelity=0.82,
        probability_deviation=0.08,
        z_score=3.2,
        p_value=0.001,
        chi2_statistic=10.5,
        signer_valid=True,
        nonce_valid=True,
        session_valid=True,
        replayed_nonce=False,
        impersonation_flag=False,
        shots=1000
    )
    vec = extract_feature_vector(evt)
    assert len(vec) == 11
    # Check values match feature definitions
    assert vec[0] == 0.82  # fidelity
    assert vec[1] == 0.08  # probability_deviation
    assert vec[2] == 3.2   # z_score
    assert vec[3] == 0.001 # p_value
    assert vec[4] == 10.5  # chi2_statistic
    assert vec[5] == 1.0   # signer_valid
    assert vec[6] == 1.0   # nonce_valid
    assert vec[7] == 1.0   # session_valid
    assert vec[8] == 0.0   # replayed_nonce
    assert vec[9] == 0.0   # impersonation_flag
    assert vec[10] == 0.2  # shots_normalized (1000 / 5000)


def test_onnx_model_graph_spec():
    """Assert ONNX model has input shape [None, 11] and outputs 3 classes."""
    clf = get_default_classifier()
    assert clf.ort_session is not None
    
    inputs = clf.ort_session.get_inputs()
    assert len(inputs) == 1
    assert inputs[0].shape == ['float_input_dim_0', 11] or inputs[0].shape == [None, 11] or inputs[0].shape[1] == 11
    
    evt = SecurityEvent(fidelity=0.95, shots=1000)
    res = clf.predict(evt)
    assert len(res["confidence_scores"]) == 3
    assert set(res["confidence_scores"].keys()) == {"NORMAL", "SUSPICIOUS", "ATTACK"}
    assert "CPU" in res["execution_provider"]


def test_deterministic_decision_preservation():
    """Assert AI prediction does NOT modify or override deterministic QDS decision."""
    evt = SecurityEvent(
        fidelity=0.95,
        deterministic_decision="ACCEPT",
        deterministic_reasons=["Verification passed"]
    )
    payload = analyze_and_triage_event(evt)
    assert payload["deterministic_verification"]["decision"] == "ACCEPT"

    evt_reject = SecurityEvent(
        replayed_nonce=True,
        nonce_valid=False,
        deterministic_decision="REJECT",
        deterministic_reasons=["Freshness check failed"]
    )
    payload_reject = analyze_and_triage_event(evt_reject)
    assert payload_reject["deterministic_verification"]["decision"] == "REJECT"
    assert payload_reject["triage"]["priority"] == "P1 - CRITICAL THREAT"


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

