"""
NIST Post-Quantum Cryptography (PQC) Signature Analysis & Comparison Model.
SIH26141 • Egreen Quanta

Models NIST standardized PQC digital signature schemes (ML-DSA, SLH-DSA)
and compares key sizes, signature overhead, and quantum security against classical schemes.
"""

from typing import Dict, Any, List, Optional


PQC_DATABASE: Dict[str, Dict[str, Any]] = {
    "ML-DSA-44": {
        "name": "ML-DSA-44",
        "family": "Module-Lattice (Dilithium)",
        "standard": "FIPS 204",
        "nist_security_category": 1,
        "classical_security_bits": 128,
        "quantum_security_bits": 128,
        "public_key_bytes": 1312,
        "private_key_bytes": 2560,
        "signature_bytes": 2420,
        "mathematical_foundation": "Module Learning With Errors (M-LWE) & Module Short Integer Solution (M-SIS)",
        "quantum_threat_classification": "Quantum-Resistant",
        "status": "NIST Standardized (2024)",
        "description": "Primary recommended general-purpose PQC signature scheme for security category 1.",
    },
    "ML-DSA-65": {
        "name": "ML-DSA-65",
        "family": "Module-Lattice (Dilithium)",
        "standard": "FIPS 204",
        "nist_security_category": 3,
        "classical_security_bits": 192,
        "quantum_security_bits": 192,
        "public_key_bytes": 1952,
        "private_key_bytes": 4032,
        "signature_bytes": 3309,
        "mathematical_foundation": "Module Learning With Errors (M-LWE) & Module Short Integer Solution (M-SIS)",
        "quantum_threat_classification": "Quantum-Resistant",
        "status": "NIST Standardized (2024)",
        "description": "Primary recommended PQC signature scheme for security category 3.",
    },
    "ML-DSA-87": {
        "name": "ML-DSA-87",
        "family": "Module-Lattice (Dilithium)",
        "standard": "FIPS 204",
        "nist_security_category": 5,
        "classical_security_bits": 256,
        "quantum_security_bits": 256,
        "public_key_bytes": 2592,
        "private_key_bytes": 4896,
        "signature_bytes": 4627,
        "mathematical_foundation": "Module Learning With Errors (M-LWE) & Module Short Integer Solution (M-SIS)",
        "quantum_threat_classification": "Quantum-Resistant",
        "status": "NIST Standardized (2024)",
        "description": "High-security PQC signature scheme for security category 5.",
    },
    "SLH-DSA-128f": {
        "name": "SLH-DSA-128f",
        "family": "Stateless Hash-Based (SPHINCS+)",
        "standard": "FIPS 205",
        "nist_security_category": 1,
        "classical_security_bits": 128,
        "quantum_security_bits": 128,
        "public_key_bytes": 32,
        "private_key_bytes": 64,
        "signature_bytes": 17088,
        "mathematical_foundation": "Cryptographic Hash Functions (SHAKE-256 / SHA-256)",
        "quantum_threat_classification": "Quantum-Resistant",
        "status": "NIST Standardized (2024)",
        "description": "Stateless hash-based signature scheme optimized for fast signing.",
    },
    "SLH-DSA-128s": {
        "name": "SLH-DSA-128s",
        "family": "Stateless Hash-Based (SPHINCS+)",
        "standard": "FIPS 205",
        "nist_security_category": 1,
        "classical_security_bits": 128,
        "quantum_security_bits": 128,
        "public_key_bytes": 32,
        "private_key_bytes": 64,
        "signature_bytes": 7856,
        "mathematical_foundation": "Cryptographic Hash Functions (SHAKE-256 / SHA-256)",
        "quantum_threat_classification": "Quantum-Resistant",
        "status": "NIST Standardized (2024)",
        "description": "Stateless hash-based signature scheme optimized for small signature size.",
    },
    "SLH-DSA-256f": {
        "name": "SLH-DSA-256f",
        "family": "Stateless Hash-Based (SPHINCS+)",
        "standard": "FIPS 205",
        "nist_security_category": 5,
        "classical_security_bits": 256,
        "quantum_security_bits": 256,
        "public_key_bytes": 64,
        "private_key_bytes": 128,
        "signature_bytes": 49856,
        "mathematical_foundation": "Cryptographic Hash Functions (SHAKE-256 / SHA-256)",
        "quantum_threat_classification": "Quantum-Resistant",
        "status": "NIST Standardized (2024)",
        "description": "High-security hash-based signature scheme for category 5.",
    },
}


CLASSICAL_COMPARISON_BASELINE = {
    "RSA-2048": {
        "public_key_bytes": 256,
        "private_key_bytes": 1184,
        "signature_bytes": 256,
        "quantum_threat_classification": "Vulnerable (Shor's Algorithm)",
    },
    "ECDSA-P256": {
        "public_key_bytes": 64,
        "private_key_bytes": 32,
        "signature_bytes": 64,
        "quantum_threat_classification": "Vulnerable (Shor's Algorithm)",
    },
}


def list_pqc_schemes() -> List[str]:
    """Returns list of supported PQC scheme identifiers."""
    return list(PQC_DATABASE.keys())


def get_pqc_scheme_metadata(scheme_name: str = "ML-DSA-44") -> Dict[str, Any]:
    """
    Returns full metadata for a given PQC signature scheme.

    Args:
        scheme_name: Identifier of PQC scheme (e.g., 'ML-DSA-44', 'SLH-DSA-128f').

    Returns:
        Dictionary containing metadata, sizes, and security classifications.
    """
    if scheme_name not in PQC_DATABASE:
        scheme_name = "ML-DSA-44"

    meta = PQC_DATABASE[scheme_name].copy()
    
    # Calculate comparative ratios against ECDSA-P256
    ecdsa_pub = CLASSICAL_COMPARISON_BASELINE["ECDSA-P256"]["public_key_bytes"]
    ecdsa_sig = CLASSICAL_COMPARISON_BASELINE["ECDSA-P256"]["signature_bytes"]

    meta["pubkey_overhead_vs_ecdsa"] = round(meta["public_key_bytes"] / ecdsa_pub, 2)
    meta["sig_overhead_vs_ecdsa"] = round(meta["signature_bytes"] / ecdsa_sig, 2)
    meta["scientific_framing_notice"] = (
        "Designed to resist known classical and quantum attack strategies; "
        "not claimed as mathematically proven unbreakable."
    )

    return meta
