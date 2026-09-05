"""
Reproducible Research Experiment: ECC Discrete Log Quantum Threat Analysis.
SIH26141 • Egreen Quanta
"""

import os
import json
from qds_detector.quantum_attacks.ecc_analysis import analyze_ecc_dlog_threat


def run_ecc_experiment_suite() -> str:
    """Executes ECC discrete log attacks on toy curves and saves JSON report."""
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "experiments", "results")
    os.makedirs(results_dir, exist_ok=True)

    curves = ["toy_p17", "toy_p23"]
    experiment_data = []

    for c in curves:
        res = analyze_ecc_dlog_threat(curve_name=c)
        experiment_data.append(res)

    out_file = os.path.abspath(os.path.join(results_dir, "ecc_dlog_results.json"))
    with open(out_file, "w") as f:
        json.dump(experiment_data, f, indent=2)

    return out_file


if __name__ == "__main__":
    path = run_ecc_experiment_suite()
    print(f"ECC DLog research experiment saved to: {path}")
