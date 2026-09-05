"""
Unified Deterministic Quantum Risk Engine for Digital Signature Architectures.
SIH26141 • Egreen Quanta

Evaluates quantum threat vectors, attack feasibility, estimated CRQC resources,
and key size overhead to compute transparent, deterministic risk scores (NO AI/ML).
"""

from typing import Dict, Any, Optional
from qds_detector.quantum_attacks.resource_estimator import estimate_crqc_resources


RISK_LEVEL_LOW = "LOW"
RISK_LEVEL_MODERATE = "MODERATE"
RISK_LEVEL_HIGH = "HIGH"
RISK_LEVEL_CRITICAL = "CRITICAL"


ALGORITHM_VULNERABILITY_CATALOG = {
    "RSA-1024": {
        "family": "Classical Asymmetric",
        "attack_family": "Shor Factorization",
        "vulnerability_score": 1.0,  # Highly vulnerable
        "attack_maturity": "Theoretical Complete Break",
        "pqc_status": "Vulnerable",
        "action": "Immediate Migration Required",
    },
    "RSA-2048": {
        "family": "Classical Asymmetric",
        "attack_family": "Shor Factorization",
        "vulnerability_score": 1.0,
        "attack_maturity": "Theoretical Complete Break",
        "pqc_status": "Vulnerable",
        "action": "High-Priority Migration to PQC / QDS",
    },
    "RSA-4096": {
        "family": "Classical Asymmetric",
        "attack_family": "Shor Factorization",
        "vulnerability_score": 1.0,
        "attack_maturity": "Theoretical Complete Break",
        "pqc_status": "Vulnerable",
        "action": "Planned Migration to PQC / QDS",
    },
    "ECDSA-P256": {
        "family": "Classical Asymmetric",
        "attack_family": "Shor Discrete Log",
        "vulnerability_score": 1.0,
        "attack_maturity": "Theoretical Complete Break",
        "pqc_status": "Vulnerable",
        "action": "High-Priority Migration to PQC / QDS",
    },
    "ECDSA-P384": {
        "family": "Classical Asymmetric",
        "attack_family": "Shor Discrete Log",
        "vulnerability_score": 1.0,
        "attack_maturity": "Theoretical Complete Break",
        "pqc_status": "Vulnerable",
        "action": "Planned Migration to PQC / QDS",
    },
    "Ed25519": {
        "family": "Classical Asymmetric",
        "attack_family": "Shor Discrete Log",
        "vulnerability_score": 1.0,
        "attack_maturity": "Theoretical Complete Break",
        "pqc_status": "Vulnerable",
        "action": "High-Priority Migration to PQC / QDS",
    },
    "ML-DSA-44": {
        "family": "Post-Quantum (Lattice)",
        "attack_family": "Lattice Reduction (SVP/CVP)",
        "vulnerability_score": 0.0,
        "attack_maturity": "Resistant to Known Attacks",
        "pqc_status": "Quantum-Resistant",
        "action": "Maintain & Monitor NIST Guidelines",
    },
    "SLH-DSA-128f": {
        "family": "Post-Quantum (Hash-Based)",
        "attack_family": "Grover Preimage Search",
        "vulnerability_score": 0.1,
        "attack_maturity": "Resistant to Known Attacks",
        "pqc_status": "Quantum-Resistant",
        "action": "Maintain & Monitor NIST Guidelines",
    },
    "QDS-Teleportation": {
        "family": "Quantum Signature (Physical)",
        "attack_family": "Quantum State Forgery & Noise",
        "vulnerability_score": 0.05,
        "attack_maturity": "Physical Information-Theoretic Security",
        "pqc_status": "Quantum-Native",
        "action": "Deploy Q-Sentinel Threat Monitoring Engine",
    },
}


def evaluate_quantum_risk(
    algorithm_name: str = "RSA-2048",
    data_retention_years: int = 10,
    infrastructure_lifecycle_years: int = 5
) -> Dict[str, Any]:
    """
    Evaluates quantum security risk deterministically without AI/ML.

    Calculates:
    - Mathematical Quantum Vulnerability
    - Current Physical Feasibility vs CRQC Timeline
    - Mosca 'Store-Now-Decrypt-Later' / Forgery Migration Horizon (X + Y > Z)
    - Unified Risk Level (LOW, MODERATE, HIGH, CRITICAL)

    Args:
        algorithm_name: Name of target signature scheme (e.g. RSA-2048, ECDSA-P256, ML-DSA-44).
        data_retention_years: Number of years signature integrity/confidentiality must persist (X).
        infrastructure_lifecycle_years: Years required to migrate infrastructure to PQC (Y).

    Returns:
        Dictionary containing score breakdown, risk level, migration priority, and rationale.
    """
    catalog_info = ALGORITHM_VULNERABILITY_CATALOG.get(
        algorithm_name,
        ALGORITHM_VULNERABILITY_CATALOG["RSA-2048"]
    )

    vuln_score = catalog_info["vulnerability_score"]
    
    # Estimate CRQC physical resources if applicable
    if vuln_score > 0.5:
        resource_est = estimate_crqc_resources(algorithm_name)
        logical_qubits = resource_est["logical_qubits"]
        physical_qubits = resource_est["total_estimated_physical_qubits"]
    else:
        resource_est = None
        logical_qubits = 0
        physical_qubits = 0

    # Mosca Theorem Horizon Calculation:
    # X = data retention years
    # Y = migration years
    # Z = estimated years until CRQC (assumed baseline ~ 15 years for CRQC estimate)
    estimated_years_to_crqc = 15.0
    mosca_sum = data_retention_years + infrastructure_lifecycle_years
    mosca_urgency = mosca_sum > estimated_years_to_crqc

    # Deterministic Risk Categorization Logic
    if vuln_score == 0.0 or vuln_score <= 0.1:
        risk_level = RISK_LEVEL_LOW
        overall_score = 10.0
    elif vuln_score < 0.3:
        risk_level = RISK_LEVEL_MODERATE
        overall_score = 35.0
    else:
        if mosca_urgency:
            risk_level = RISK_LEVEL_CRITICAL
            overall_score = 95.0
        else:
            risk_level = RISK_LEVEL_HIGH
            overall_score = 75.0

    return {
        "algorithm_name": algorithm_name,
        "family": catalog_info["family"],
        "attack_family": catalog_info["attack_family"],
        "mathematical_quantum_vulnerability": catalog_info["pqc_status"],
        "vulnerability_score_numeric": vuln_score,
        "overall_risk_score_100": overall_score,
        "risk_level": risk_level,
        "action_recommendation": catalog_info["action"],
        "mosca_theorem_analysis": {
            "data_retention_years_X": data_retention_years,
            "migration_duration_years_Y": infrastructure_lifecycle_years,
            "estimated_years_to_crqc_Z": estimated_years_to_crqc,
            "mosca_threshold_exceeded": mosca_urgency,
            "formula_status": f"X ({data_retention_years}) + Y ({infrastructure_lifecycle_years}) = {mosca_sum} {' > ' if mosca_urgency else ' <= '} Z ({estimated_years_to_crqc})"
        },
        "resource_estimates": {
            "logical_qubits_required": logical_qubits,
            "physical_qubits_required": physical_qubits,
        },
        "scientific_framing": {
            "algorithmically_vulnerable": vuln_score > 0.5,
            "currently_practically_breakable": False,  # CRQC does not exist today
            "notes": (
                f"Distinguishes mathematical vulnerability under Shor/Grover from practical current capability. "
                f"Current noisy intermediate-scale quantum (NISQ) devices cannot execute full fault-tolerant "
                f"circuits for {algorithm_name}."
            )
        }
    }
