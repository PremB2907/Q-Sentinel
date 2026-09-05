"""
Reproducible Research Experiment: Grover Search Complexity Analysis.
SIH26141 • Egreen Quanta
"""

import os
import json
from qds_detector.quantum_attacks.grover import run_grover_search_analysis


def run_grover_experiment_suite() -> str:
    """Executes Grover search across key space dimensions and saves JSON report."""
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "experiments", "results")
    os.makedirs(results_dir, exist_ok=True)

    key_spaces = [4, 6, 8, 10, 12]
    experiment_data = []

    for k in key_spaces:
        res = run_grover_search_analysis(key_space_bits=k)
        experiment_data.append(res)

    out_file = os.path.abspath(os.path.join(results_dir, "grover_search_results.json"))
    with open(out_file, "w") as f:
        json.dump(experiment_data, f, indent=2)

    return out_file


if __name__ == "__main__":
    path = run_grover_experiment_suite()
    print(f"Grover search research experiment saved to: {path}")
