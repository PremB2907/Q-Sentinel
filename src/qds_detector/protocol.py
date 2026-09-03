"""
End-to-End Quantum Digital Signature (QDS) Teleportation & Threat Detection Pipeline.

Orchestrates state preparation, Bell pair entanglement, teleportation, channel noise,
attack transformations, projective measurements, fidelity calculation, and deterministic threat decision.
"""

import time
from typing import Dict, Any
from qiskit.quantum_info import Statevector, DensityMatrix

from qds_detector.config import ExperimentConfig, SessionContext, ThresholdConfig
from qds_detector.states import get_statevector, get_density_matrix, get_expected_probabilities, calculate_fidelity, STATE_ALIASES
from qds_detector.teleportation import run_teleportation_experiment
from qds_detector.attacks import (
    simulate_attack_counts,
    apply_forgery_attack,
    apply_channel_attack,
    apply_replay_attack,
    apply_impersonation_attack
)
from qds_detector.detector import evaluate_threat_detection
from qds_detector.reporting import create_experiment_record


def run_qds_experiment(config: ExperimentConfig) -> Dict[str, Any]:
    """
    Execute full QDS Teleportation Threat Detection Pipeline.
    """
    start_time = time.perf_counter()
    
    state_name = STATE_ALIASES.get(config.input_state, config.input_state)
    basis = config.measurement_basis.upper()
    baseline_probs = get_expected_probabilities(state_name, basis)
    
    # 1. Setup Session Context & Apply Protocol Attacks if selected
    context = config.session_context
    context.validate()
    
    if config.attack_type == "replay":
        context = apply_replay_attack(context)
    elif config.attack_type == "impersonation":
        context = apply_impersonation_attack(context)

    # 2. Run Quantum Experiment / Attack Transformation
    if config.attack_type == "none" or config.attack_severity == 0.0:
        # Clean teleportation run via Qiskit Aer
        teleport_res = run_teleportation_experiment(
            input_state=state_name,
            measurement_basis=basis,
            shots=config.shots,
            seed=config.seed
        )
        counts = teleport_res["counts"]
        obs_probs = teleport_res["observed_probabilities"]
        
        # In clean run, received state = input state (Fidelity = 1.0)
        sv_in = get_statevector(state_name)
        fidelity = calculate_fidelity(sv_in, sv_in)
        
    elif config.attack_type == "forgery":
        rho_attack, _ = apply_forgery_attack(state_name, config.attack_severity)
        sv_in = get_statevector(state_name)
        fidelity = calculate_fidelity(sv_in, rho_attack)
        
        sim_res = simulate_attack_counts(
            input_state=state_name,
            basis=basis,
            attack_type="forgery",
            severity=config.attack_severity,
            shots=config.shots,
            seed=config.seed
        )
        counts = sim_res["counts"]
        obs_probs = sim_res["observed_probabilities"]
        
    elif config.attack_type.startswith("channel_"):
        ch_name = config.attack_type.replace("channel_", "")
        rho_noisy, _ = apply_channel_attack(state_name, ch_name, config.attack_severity)
        sv_in = get_statevector(state_name)
        fidelity = calculate_fidelity(sv_in, rho_noisy)
        
        sim_res = simulate_attack_counts(
            input_state=state_name,
            basis=basis,
            attack_type=config.attack_type,
            severity=config.attack_severity,
            shots=config.shots,
            seed=config.seed
        )
        counts = sim_res["counts"]
        obs_probs = sim_res["observed_probabilities"]
        
    else:
        # Protocol layer attack (replay / impersonation) without quantum state change
        teleport_res = run_teleportation_experiment(
            input_state=state_name,
            measurement_basis=basis,
            shots=config.shots,
            seed=config.seed
        )
        counts = teleport_res["counts"]
        obs_probs = teleport_res["observed_probabilities"]
        sv_in = get_statevector(state_name)
        fidelity = calculate_fidelity(sv_in, sv_in)

    # 3. Evaluate Two-Tier Deterministic Threat Detector
    detection = evaluate_threat_detection(
        observed_counts=counts,
        baseline_probs=baseline_probs,
        fidelity=fidelity,
        context=context,
        basis=basis,
        thresholds=config.thresholds
    )
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    
    config_dict = {
        "input_state": state_name,
        "measurement_basis": basis,
        "shots": config.shots,
        "seed": config.seed,
        "attack_type": config.attack_type,
        "attack_severity": config.attack_severity,
    }
    
    exp_record = create_experiment_record(
        exp_id=f"EXP-{int(time.time()*1000)}",
        config_dict=config_dict,
        detection_result=detection.to_dict(),
        execution_time_ms=elapsed_ms
    )
    
    # Expose evidence dict and threat category for UI and telemetry
    exp_record["evidence"] = detection.evidence
    exp_record["threat_category"] = detection.threat_category
    
    return exp_record
