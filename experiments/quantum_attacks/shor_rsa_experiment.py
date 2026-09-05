"""
Reproducible Research Experiment: Shor's Factorization on Toy Semiprimes.
SIH26141 • Egreen Quanta
"""

import os
import json
from qds_detector.quantum_attacks.shor import run_shor_factorization


def run_shor_experiment_suite() -> str:
    """Executes Shor factorization across toy semiprimes and saves JSON report."""
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "experiments", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    semiprimes = [15, 21, 35, 77]
    experiment_data = []

    for N in semiprimes:
        res = run_shor_factorization(N=N)
        experiment_data.append(res)

    out_file = os.path.abspath(os.path.join(results_dir, "shor_rsa_results.json"))
    with open(out_file, "w") as f:
        json.dump(experiment_data, f, indent=2)

    return out_file


if __name__ == "__main__":
    path = run_shor_experiment_suite()
    print(f"Shor RSA research experiment saved to: {path}")
