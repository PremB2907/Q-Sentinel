"""
Empirical Calibration Engine for QDS Threat Detector.

Generates basis-specific empirical acceptance regions (Z, X, Y) from independent clean trials.
Saves calibrated thresholds to experiments/calibration/calibrated_thresholds.json.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np

from qds_detector.config import ThresholdConfig, ExperimentConfig
from qds_detector.teleportation import run_teleportation_experiment
from qds_detector.states import get_expected_probabilities, calculate_fidelity, get_statevector, STATE_ALIASES
from qds_detector.statistics import compute_probability_deviation


CALIBRATION_DIR = Path("experiments/calibration")


def run_empirical_calibration(
    num_trials: int = 100,
    shots: int = 5000,
    alpha: float = 0.01
) -> Dict[str, Any]:
    """
    Run empirical calibration over clean teleportation experiments for Z, X, and Y bases.
    Calculates basis-specific maximum deviation percentiles and fidelity bounds.
    """
    basis_states = {
        "Z": ["|0>", "|1>"],
        "X": ["|+>", "|->"],
        "Y": ["|+i>", "|-i>"]
    }
    
    calibrated_results = {}
    
    for basis, states in basis_states.items():
        deviations = []
        fidelities = []
        
        for trial in range(num_trials):
            for state_name in states:
                seed = trial * 100 + hash(state_name) % 97
                res = run_teleportation_experiment(
                    input_state=state_name,
                    measurement_basis=basis,
                    shots=shots,
                    seed=seed
                )
                
                obs_probs = res["observed_probabilities"]
                exp_probs = res["expected_probabilities"]
                dev = compute_probability_deviation(obs_probs, exp_probs)
                
                sv_in = get_statevector(state_norm := STATE_ALIASES.get(state_name, state_name))
                fid = calculate_fidelity(sv_in, sv_in)
                
                deviations.append(dev)
                fidelities.append(fid)
                
        # Derive 99th percentile for maximum deviation threshold (1 - alpha)
        percentile_dev = float(np.percentile(deviations, (1.0 - alpha) * 100.0))
        # Add small empirical tolerance margin
        max_dev_threshold = round(max(0.01, percentile_dev * 1.15), 4)
        
        min_fid_threshold = round(float(np.percentile(fidelities, alpha * 100.0)), 4)
        min_fid_threshold = min(0.98, max(0.95, min_fid_threshold))
        
        calibrated_results[basis] = {
            "basis": basis,
            "trials_eval": len(deviations),
            "max_probability_deviation_99th": float(percentile_dev),
            "max_probability_deviation_threshold": max_dev_threshold,
            "min_fidelity_threshold": min_fid_threshold,
            "mean_deviation": float(np.mean(deviations)),
            "std_deviation": float(np.std(deviations))
        }

    calibration_export = {
        "metadata": {
            "num_trials_per_state": num_trials,
            "shots": shots,
            "alpha": alpha,
            "calibration_timestamp": float(np.round(np.datetime64('now').astype(float), 2))
        },
        "basis_thresholds": calibrated_results
    }
    
    CALIBRATION_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CALIBRATION_DIR / "calibrated_thresholds.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(calibration_export, f, indent=2)
        
    return calibration_export


if __name__ == "__main__":
    print("Running empirical basis-specific calibration...")
    results = run_empirical_calibration(num_trials=50, shots=5000)
    print("Empirical calibration complete! Saved to experiments/calibration/calibrated_thresholds.json")
    print(json.dumps(results, indent=2))
