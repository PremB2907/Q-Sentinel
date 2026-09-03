"""
Multi-Trial Evaluation Benchmark Suite for QDS Threat Detector.

Evaluates performance across:
Attack x Severity x Basis x Shots x Trials

Computes TPR, FPR, FAR, FRR, FNR, state fidelity, and execution latency.
Outputs reproducible benchmark JSON to experiments/results/benchmark_results.json.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List
import numpy as np

from qds_detector.config import ExperimentConfig, ThresholdConfig, SessionContext
from qds_detector.protocol import run_qds_experiment
from qds_detector.metrics import compute_batch_metrics


RESULTS_DIR = Path("experiments/results")


def run_benchmark_suite(
    num_trials: int = 20,
    shots: int = 5000,
    severities: List[float] | None = None
) -> Dict[str, Any]:
    """
    Execute multi-trial evaluation benchmark suite.
    Ensures non-overlapping dataset from calibration runs.
    """
    if severities is None:
        severities = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        
    attack_types = [
        "none",
        "forgery",
        "channel_bit_flip",
        "channel_phase_flip",
        "channel_depolarizing",
        "replay",
        "impersonation"
    ]
    
    bases = ["Z", "X", "Y"]
    state_basis_map = {
        "Z": "|0>",
        "X": "|+>",
        "Y": "|+i>"
    }
    
    all_experiment_results = []
    summary_by_attack = {}
    
    start_bench_time = time.perf_counter()
    
    for attack in attack_types:
        attack_records = []
        
        for sev in (severities if attack not in ["none", "replay", "impersonation"] else [0.0]):
            for basis in bases:
                input_state = state_basis_map[basis]
                
                for trial in range(num_trials):
                    # Use distinct seed offset for evaluation benchmark
                    seed = 1000 + trial * 37 + int(sev * 100) + hash(basis) % 89
                    
                    cfg = ExperimentConfig(
                        input_state=input_state,
                        measurement_basis=basis,
                        shots=shots,
                        seed=seed,
                        attack_type=attack,
                        attack_severity=float(sev)
                    )
                    
                    record = run_qds_experiment(cfg)
                    attack_records.append(record)
                    all_experiment_results.append(record)
                    
        batch_m = compute_batch_metrics(attack_records)
        summary_by_attack[attack] = batch_m.to_dict()

    total_bench_time = time.perf_counter() - start_bench_time
    overall_m = compute_batch_metrics(all_experiment_results)
    
    benchmark_export = {
        "metadata": {
            "num_trials_per_config": num_trials,
            "shots": shots,
            "total_experiments_evaluated": len(all_experiment_results),
            "benchmark_execution_time_seconds": round(total_bench_time, 2)
        },
        "overall_metrics": overall_m.to_dict(),
        "summary_by_attack_scenario": summary_by_attack
    }
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "benchmark_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_export, f, indent=2)
        
    return benchmark_export


if __name__ == "__main__":
    print("Executing QDS Threat Detector Multi-Trial Benchmark Suite...")
    res = run_benchmark_suite(num_trials=10, shots=5000)
    print(f"Benchmark complete! Total experiments evaluated: {res['metadata']['total_experiments_evaluated']}")
    print(f"Overall Accuracy: {res['overall_metrics']['accuracy']*100:.2f}% | False Accept Rate (FAR): {res['overall_metrics']['far']*100:.2f}% | False Reject Rate (FRR): {res['overall_metrics']['frr']*100:.2f}%")
