"""
Severity-Wise Benchmark & Sensitivity Curve Suite for QDS Threat Detector.

Evaluates exact Detection Rate (%) vs Attack Strength lambda in [0.00, 0.05, 0.10, ..., 1.00]
for:
1. State Forgery
2. Depolarizing Channel Noise
3. Bit-Flip Noise
4. Phase-Flip Noise

Outputs structured severity sweep data to experiments/results/severity_sweep_benchmark.json.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List
import numpy as np

from qds_detector.config import ExperimentConfig, ThresholdConfig
from qds_detector.protocol import run_qds_experiment


RESULTS_DIR = Path("experiments/results")


def run_severity_sweep_benchmark(
    trials_per_step: int = 30,
    shots: int = 5000
) -> Dict[str, Any]:
    """
    Run high-resolution severity sweep for all quantum attack vectors.
    """
    severities = [round(x, 2) for x in np.linspace(0.0, 1.0, 21)]
    quantum_attacks = ["forgery", "channel_depolarizing", "channel_bit_flip", "channel_phase_flip"]
    bases = ["Z", "X", "Y"]
    state_basis_map = {"Z": "|0>", "X": "|+>", "Y": "|+i>"}
    
    sweep_results = {}
    
    start_time = time.perf_counter()
    
    for attack in quantum_attacks:
        attack_curve = []
        
        for sev in severities:
            detected_count = 0
            total_trials = 0
            fidelities = []
            deviations = []
            
            for basis in bases:
                input_state = state_basis_map[basis]
                
                for trial in range(trials_per_step):
                    seed = 5000 + trial * 41 + int(sev * 100) + hash(basis) % 97
                    cfg = ExperimentConfig(
                        input_state=input_state,
                        measurement_basis=basis,
                        shots=shots,
                        seed=seed,
                        attack_type=attack,
                        attack_severity=float(sev)
                    )
                    rec = run_qds_experiment(cfg)
                    
                    total_trials += 1
                    fidelities.append(rec["fidelity"])
                    deviations.append(rec["deviation"])
                    
                    if rec["decision"] in ["REJECT", "SUSPICIOUS"]:
                        detected_count += 1
                        
            det_rate = (detected_count / total_trials) * 100.0
            attack_curve.append({
                "severity": float(sev),
                "trials": total_trials,
                "detection_rate_pct": round(det_rate, 2),
                "false_accept_rate_pct": round(100.0 - det_rate, 2),
                "mean_fidelity": round(float(np.mean(fidelities)), 4),
                "mean_deviation": round(float(np.mean(deviations)), 4)
            })
            
        sweep_results[attack] = attack_curve

    total_time = time.perf_counter() - start_time
    
    export_data = {
        "metadata": {
            "trials_per_step_per_basis": trials_per_step,
            "total_trials_per_severity_step": trials_per_step * len(bases),
            "shots": shots,
            "severities_evaluated": severities,
            "execution_time_seconds": round(total_time, 2)
        },
        "severity_curves": sweep_results
    }
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "severity_sweep_benchmark.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)
        
    return export_data


if __name__ == "__main__":
    print("Executing High-Resolution Severity Sweep Benchmark Suite...")
    res = run_severity_sweep_benchmark(trials_per_step=20, shots=5000)
    print("Severity sweep complete! Results saved to experiments/results/severity_sweep_benchmark.json")
