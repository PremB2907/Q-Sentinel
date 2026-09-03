"""
Empirical Calibration Engine for QDS Threat Detector.

Provides two calibration modes:
1. Ideal-Channel Calibration: Zero physical noise baseline
2. Noise-Aware Calibration: Defined physical quantum channel noise baseline (p_noise > 0)

Outputs basis-specific empirical acceptance regions (Z, X, Y) saved to:
experiments/calibration/calibrated_thresholds.json
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np

from qds_detector.config import ThresholdConfig, ExperimentConfig
from qds_detector.teleportation import run_teleportation_experiment
from qds_detector.states import get_expected_probabilities, calculate_fidelity, get_statevector, STATE_ALIASES
from qds_detector.statistics import compute_probability_deviation
from qds_detector.channels import apply_depolarizing_channel
from qds_detector.measurements import evaluate_state_projective_probabilities


CALIBRATION_DIR = Path("experiments/calibration")


def run_empirical_calibration(
    num_trials: int = 100,
    shots: int = 5000,
    alpha: float = 0.01,
    p_noise: float = 0.0  # Set > 0.0 for Noise-Aware calibration
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
                
                if p_noise <= 0.0:
                    # Ideal clean run
                    res = run_teleportation_experiment(
                        input_state=state_name,
                        measurement_basis=basis,
                        shots=shots,
                        seed=seed
                    )
                    obs_probs = res["observed_probabilities"]
                    exp_probs = res["expected_probabilities"]
                    sv_in = get_statevector(state_norm := STATE_ALIASES.get(state_name, state_name))
                    fid = calculate_fidelity(sv_in, sv_in)
                else:
                    # Noise-aware run with defined physical noise p_noise
                    state_norm = STATE_ALIASES.get(state_name, state_name)
                    sv_in = get_statevector(state_norm)
                    rho_noisy = apply_depolarizing_channel(sv_in, p_noise)
                    fid = calculate_fidelity(sv_in, rho_noisy)
                    
                    probs_theory = evaluate_state_projective_probabilities(rho_noisy, basis)
                    rng = np.random.default_rng(seed)
                    k_plus = int(rng.binomial(n=shots, p=probs_theory["+1"]))
                    obs_probs = {"+1": k_plus / shots, "-1": (shots - k_plus) / shots}
                    exp_probs = get_expected_probabilities(state_norm, basis)
                    
                dev = compute_probability_deviation(obs_probs, exp_probs)
                deviations.append(dev)
                fidelities.append(fid)
                
        # Derive 99th percentile for maximum deviation threshold (1 - alpha)
        percentile_dev = float(np.percentile(deviations, (1.0 - alpha) * 100.0))
        max_dev_threshold = round(max(0.01, percentile_dev * 1.15), 4)
        
        min_fid_threshold = round(float(np.percentile(fidelities, alpha * 100.0)), 4)
        min_fid_threshold = min(0.98, max(0.90, min_fid_threshold))
        
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
            "p_noise_channel": p_noise,
            "calibration_mode": "Ideal-Channel" if p_noise == 0.0 else "Noise-Aware"
        },
        "basis_thresholds": calibrated_results
    }
    
    CALIBRATION_DIR.mkdir(parents=True, exist_ok=True)
    mode_filename = "calibrated_thresholds.json" if p_noise == 0.0 else "noise_aware_thresholds.json"
    out_path = CALIBRATION_DIR / mode_filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(calibration_export, f, indent=2)
        
    return calibration_export


if __name__ == "__main__":
    print("Executing Ideal-Channel Empirical Calibration...")
    res_ideal = run_empirical_calibration(num_trials=50, shots=5000, p_noise=0.0)
    print("Executing Noise-Aware Empirical Calibration (p_noise=0.005)...")
    res_noisy = run_empirical_calibration(num_trials=50, shots=5000, p_noise=0.005)
    print("Calibrations complete! Saved to experiments/calibration/")
