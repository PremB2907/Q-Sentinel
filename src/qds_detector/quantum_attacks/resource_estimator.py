"""
Cryptographically Relevant Quantum Computer (CRQC) Resource Estimator.
SIH26141 • Egreen Quanta

Estimates logical qubits, T-gate depth, surface-code physical qubits,
and estimated execution runtime for cracking classical signature algorithms (RSA & ECDSA).
"""

import math
from typing import Dict, Any, List


# Standard cryptographic target parameter profiles
SCHEME_PROFILES = {
    "RSA-1024": {"type": "RSA", "bits": 1024, "classical_security": 80},
    "RSA-2048": {"type": "RSA", "bits": 2048, "classical_security": 112},
    "RSA-3072": {"type": "RSA", "bits": 3072, "classical_security": 128},
    "RSA-4096": {"type": "RSA", "bits": 4096, "classical_security": 152},
    "ECDSA-P192": {"type": "ECDSA", "bits": 192, "classical_security": 96},
    "ECDSA-P256": {"type": "ECDSA", "bits": 256, "classical_security": 128},
    "ECDSA-P384": {"type": "ECDSA", "bits": 384, "classical_security": 192},
    "ECDSA-P521": {"type": "ECDSA", "bits": 521, "classical_security": 256},
    "Ed25519": {"type": "ECDSA", "bits": 256, "classical_security": 128},
}


def estimate_crqc_resources(
    scheme_name: str = "RSA-2048",
    physical_error_rate: float = 1e-3,
    surface_code_cycle_us: float = 1.0  # Surface code cycle time in microseconds
) -> Dict[str, Any]:
    """
    Estimates CRQC physical and logical quantum circuit resources required
    to break a target digital signature scheme using Shor's algorithm.

    Args:
        scheme_name: Name of target signature scheme (e.g. RSA-2048, ECDSA-P256).
        physical_error_rate: Assumed physical gate error rate (e.g., 10^-3).
        surface_code_cycle_us: Microseconds per physical surface code cycle.

    Returns:
        Dictionary containing logical qubits, T-gate counts, physical qubit estimates,
        and estimated physical attack runtime.
    """
    profile = SCHEME_PROFILES.get(scheme_name, SCHEME_PROFILES["RSA-2048"])
    scheme_type = profile["type"]
    n = profile["bits"]

    if scheme_type == "RSA":
        # Shor RSA Resource Formulas (Ref: Beauregard / Gidney & Ekerå 2021)
        # Logical Qubits: ~ 2n + 2
        logical_qubits = 2 * n + 2
        
        # T-gate count: ~ 32 * n^3 (approximate modular exponentiation complexity)
        t_gates = int(32 * (n ** 3))
        
        # Circuit depth / T-depth: ~ 4 * n^3
        t_depth = int(4 * (n ** 3))
        
        formula_reference = "Gidney & Ekerå (2021) / Beauregard (2002)"

    else:  # ECDSA
        # Shor ECDSA Resource Formulas (Ref: Roetteler et al. 2017 / Häner et al.)
        # Logical Qubits: ~ 9n + ceil(log2(n))
        logical_qubits = 9 * n + math.ceil(math.log2(n))
        
        # T-gate count: ~ 48 * n^3 (elliptic curve point multiplication)
        t_gates = int(48 * (n ** 3))
        
        # Circuit depth: ~ 8 * n^3
        t_depth = int(8 * (n ** 3))
        
        formula_reference = "Roetteler et al. (2017) / Proos & Zalka (2003)"

    # Physical Surface Code Qubit Expansion
    # Distance d needed: d ~ 2 * ceil(log10(t_gates)) for physical error ~ 10^-3
    code_distance = max(15, 2 * math.ceil(math.log10(max(100, t_gates))))
    physical_qubits_per_logical = 2 * (code_distance ** 2)
    
    total_physical_qubits = int(logical_qubits * physical_qubits_per_logical)

    # Physical Execution Time Calculation
    # Total physical cycles ~ T_depth * code_distance
    total_cycles = t_depth * code_distance
    execution_seconds = total_cycles * (surface_code_cycle_us * 1e-6)
    
    hours = execution_seconds / 3600.0

    return {
        "scheme_name": scheme_name,
        "algorithm_family": scheme_type,
        "key_size_bits": n,
        "classical_security_level_bits": profile["classical_security"],
        "logical_qubits": logical_qubits,
        "t_gate_count": t_gates,
        "circuit_t_depth": t_depth,
        "surface_code_distance_d": code_distance,
        "physical_qubits_per_logical": physical_qubits_per_logical,
        "total_estimated_physical_qubits": total_physical_qubits,
        "estimated_execution_time_seconds": round(execution_seconds, 2),
        "estimated_execution_time_hours": round(hours, 2),
        "physical_error_rate_assumed": physical_error_rate,
        "formula_reference": formula_reference,
        "quantum_threat_status": "Vulnerable to CRQC (Shor's Algorithm)",
        "notes": f"Physical resource estimation for breaking {scheme_name} on a fault-tolerant CRQC."
    }
