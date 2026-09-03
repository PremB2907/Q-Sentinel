"""
Attack Engine for QDS Threat Simulation.

Implements threat models specified in SIH26141 Blueprint:
1. Controlled State Forgery: State mixture model rho_attack = (1 - lambda) * rho_legit + lambda * rho_forge
2. Channel Manipulation: Injection of bit-flip, phase-flip, or depolarizing noise with parameter p = lambda
3. Replay Attack: Protocol-level replay with stale nonce / reused session context
4. Impersonation Attack: Protocol-level context mismatch (wrong signer ID)
"""

from typing import Tuple, Dict, Any
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector
from qiskit_aer import AerSimulator

from qds_detector.states import get_statevector, get_density_matrix, STATE_ALIASES
from qds_detector.config import SessionContext
from qds_detector.measurements import evaluate_state_projective_probabilities
from qds_detector.channels import (
    apply_bit_flip_channel,
    apply_phase_flip_channel,
    apply_depolarizing_channel
)


def get_orthogonal_state_name(state_name: str) -> str:
    """Return orthogonal counterpart state for forgery simulation."""
    name = STATE_ALIASES.get(state_name, state_name)
    mapping = {
        "|0>": "|1>",
        "|1>": "|0>",
        "|+>": "|->",
        "|->": "|+>",
        "|+i>": "|-i>",
        "|-i>": "|+i>",
    }
    return mapping.get(name, "|1>")


def apply_forgery_attack(
    legit_state_name: str,
    severity: float = 0.0,
    forge_state_name: str | None = None
) -> Tuple[DensityMatrix, float]:
    """
    Generate forged quantum state using mixture state model:
    rho_attack = (1 - lambda) * rho_legit + lambda * rho_forge
    
    severity: lambda in [0, 1]
    """
    severity = max(0.0, min(1.0, float(severity)))
    legit_name = STATE_ALIASES.get(legit_state_name, legit_state_name)
    
    if forge_state_name is None:
        forge_name = get_orthogonal_state_name(legit_name)
    else:
        forge_name = STATE_ALIASES.get(forge_state_name, forge_state_name)
        
    rho_legit = get_density_matrix(legit_name).data
    rho_forge = get_density_matrix(forge_name).data
    
    rho_attack = (1.0 - severity) * rho_legit + severity * rho_forge
    return DensityMatrix(rho_attack), severity


def apply_channel_attack(
    state_name: str,
    channel_type: str,
    severity: float = 0.0
) -> Tuple[DensityMatrix, float]:
    """
    Apply quantum channel manipulation attack (bit-flip, phase-flip, depolarizing).
    channel_type: "bit_flip", "phase_flip", "depolarizing"
    severity: noise probability p in [0, 1]
    """
    severity = max(0.0, min(1.0, float(severity)))
    rho_clean = get_density_matrix(state_name)
    
    ch = channel_type.lower()
    if "bit" in ch and "phase" not in ch:
        rho_noisy = apply_bit_flip_channel(rho_clean, severity)
    elif "phase" in ch:
        rho_noisy = apply_phase_flip_channel(rho_clean, severity)
    elif "depolariz" in ch:
        rho_noisy = apply_depolarizing_channel(rho_clean, severity)
    else:
        rho_noisy = apply_depolarizing_channel(rho_clean, severity)
        
    return rho_noisy, severity


def apply_replay_attack(context: SessionContext) -> SessionContext:
    """
    Simulate replay attack by reusing transcript with stale nonce / invalid freshness.
    """
    attacked_context = SessionContext(
        session_id=context.session_id,
        signer_id=context.signer_id,
        expected_signer_id=context.expected_signer_id,
        nonce=f"REPLAYED-{context.nonce}",
        timestamp=context.timestamp - 3600.0,  # 1 hour in the past
        freshness_valid=False,  # Protocol rule violation!
        identity_valid=context.identity_valid
    )
    return attacked_context


def apply_impersonation_attack(context: SessionContext, fake_signer_id: str = "Eve_Impersonator_0xBAD") -> SessionContext:
    """
    Simulate impersonation attack by presenting transcript under unauthorized signer ID.
    """
    attacked_context = SessionContext(
        session_id=context.session_id,
        signer_id=fake_signer_id,  # Unmatched identity!
        expected_signer_id=context.expected_signer_id,
        nonce=context.nonce,
        timestamp=context.timestamp,
        freshness_valid=context.freshness_valid,
        identity_valid=False  # Protocol rule violation!
    )
    return attacked_context


def simulate_attack_counts(
    input_state: str,
    basis: str,
    attack_type: str,
    severity: float,
    shots: int,
    seed: int | None = 42
) -> Dict[str, Any]:
    """
    Simulate measurement counts under selected quantum attack.
    Sample empirical counts from quantum probabilities derived after attack transformation.
    """
    state_name = STATE_ALIASES.get(input_state, input_state)
    rng = np.random.default_rng(seed)
    
    if attack_type == "forgery":
        rho_attack, _ = apply_forgery_attack(state_name, severity)
        probs = evaluate_state_projective_probabilities(rho_attack, basis)
    elif attack_type.startswith("channel_"):
        ch_name = attack_type.replace("channel_", "")
        rho_noisy, _ = apply_channel_attack(state_name, ch_name, severity)
        probs = evaluate_state_projective_probabilities(rho_noisy, basis)
    else:
        # Clean run or protocol layer attack (replay/impersonation don't alter physics)
        rho_clean = get_density_matrix(state_name)
        probs = evaluate_state_projective_probabilities(rho_clean, basis)
        
    p_plus = probs["+1"]
    p_minus = probs["-1"]
    
    # Sample counts from Binomial distribution
    k_plus = int(rng.binomial(n=shots, p=p_plus))
    k_minus = shots - k_plus
    
    counts = {"+1": k_plus, "-1": k_minus}
    obs_probs = {"+1": k_plus / shots, "-1": k_minus / shots}
    
    return {
        "counts": counts,
        "observed_probabilities": obs_probs,
        "theoretical_probabilities": probs,
        "shots": shots,
        "attack_type": attack_type,
        "severity": severity
    }
