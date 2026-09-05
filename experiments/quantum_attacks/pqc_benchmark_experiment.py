"""
Reproducible Research Experiment: Classical vs PQC vs QDS Comparative Benchmark.
SIH26141 • Egreen Quanta
"""

import os
import json
from qds_detector.quantum_attacks.resource_estimator import estimate_crqc_resources
from qds_detector.quantum_attacks.pqc_analysis import get_pqc_scheme_metadata
from qds_detector.quantum_attacks.quantum_risk import evaluate_quantum_risk


def run_pqc_benchmark_suite() -> str:
    """Runs comparative benchmark across Classical, PQC, and QDS schemes."""
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "experiments", "results")
    os.makedirs(results_dir, exist_ok=True)

    schemes = ["RSA-2048", "ECDSA-P256", "ML-DSA-44", "SLH-DSA-128f", "QDS-Teleportation"]
    benchmark_data = []

    for s in schemes:
        risk = evaluate_quantum_risk(s)
        if s in ["RSA-2048", "ECDSA-P256"]:
            crqc = estimate_crqc_resources(s)
        else:
            crqc = None

        if s in ["ML-DSA-44", "SLH-DSA-128f"]:
            pqc = get_pqc_scheme_metadata(s)
        else:
            pqc = None

        benchmark_data.append({
            "scheme": s,
            "risk_assessment": risk,
            "crqc_resources": crqc,
            "pqc_metadata": pqc
        })

    out_file = os.path.abspath(os.path.join(results_dir, "pqc_comparison_results.json"))
    with open(out_file, "w") as f:
        json.dump(benchmark_data, f, indent=2)

    return out_file


if __name__ == "__main__":
    path = run_pqc_benchmark_suite()
    print(f"PQC comparative research experiment saved to: {path}")
