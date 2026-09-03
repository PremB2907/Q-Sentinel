"""
Experiment Record Exporter & JSON / CSV Reporting Module.

Exports reproducible JSON experiment records adhering to Appendix A of the SIH26141 Blueprint.
"""

import json
import time
from typing import Dict, Any
from pathlib import Path


def create_experiment_record(
    exp_id: str,
    config_dict: Dict[str, Any],
    detection_result: Dict[str, Any],
    execution_time_ms: float
) -> Dict[str, Any]:
    """Generate structured experiment record dictionary."""
    evidence = detection_result.get("evidence", {})
    
    record = {
        "experiment_id": exp_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "backend": "AerSimulator",
        "shots": evidence.get("shots", config_dict.get("shots", 5000)),
        "seed": config_dict.get("seed", 42),
        "input_state": config_dict.get("input_state", "|0>"),
        "measurement_basis": config_dict.get("measurement_basis", "Z"),
        "attack": config_dict.get("attack_type", "none"),
        "attack_severity": config_dict.get("attack_severity", 0.0),
        "baseline_probability": evidence.get("baseline_probabilities", {}),
        "observed_probability": evidence.get("observed_probabilities", {}),
        "fidelity": evidence.get("fidelity", 1.0),
        "p_value": evidence.get("p_value", 1.0),
        "deviation": evidence.get("deviation", 0.0),
        "z_score": evidence.get("z_score", 0.0),
        "freshness_valid": evidence.get("freshness_valid", True),
        "identity_valid": evidence.get("identity_valid", True),
        "decision": detection_result.get("decision", "ACCEPT"),
        "reason": detection_result.get("reason", ""),
        "execution_time_ms": execution_time_ms
    }
    return record


def save_experiment_record(record: Dict[str, Any], filepath: str | Path) -> None:
    """Save experiment record as formatted JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
