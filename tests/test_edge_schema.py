"""
Unit tests for Q-Sentinel Edge typed SecurityEvent schema.
SIH26141 • Egreen Quanta
"""

import pytest
from qds_detector.edge_ai.schema import SecurityEvent


def test_security_event_defaults():
    evt = SecurityEvent()
    assert evt.event_id.startswith("EVT-")
    assert evt.input_state == "|0>"
    assert evt.measurement_basis == "Z"
    assert evt.deterministic_decision == "ACCEPT"
    assert evt.signer_valid is True
    assert evt.replayed_nonce is False


def test_security_event_serialization():
    evt = SecurityEvent(
        input_state="|+>",
        measurement_basis="X",
        attack_type="state_forgery",
        fidelity=0.82,
        z_score=3.45,
        deterministic_decision="REJECT",
        deterministic_reasons=["Fidelity bound breach"]
    )
    d = evt.to_dict()
    assert d["input_state"] == "|+>"
    assert d["fidelity"] == 0.82
    assert d["deterministic_decision"] == "REJECT"

    reconstructed = SecurityEvent.from_dict(d)
    assert reconstructed.input_state == "|+>"
    assert reconstructed.fidelity == 0.82
