"""
Synthetic Dataset Generator powered by Q-Sentinel Teleportation Engine.
SIH26141 • Egreen Quanta
"""

import random
from typing import List, Tuple
import numpy as np

from qds_detector.config import ExperimentConfig, SessionContext
from qds_detector.states import PAULI_STATES
from qds_detector.protocol import run_qds_experiment
from qds_detector.edge_ai.schema import SecurityEvent


LABEL_MAP = {
    "NORMAL": 0,
    "SUSPICIOUS": 1,
    "ATTACK": 2
}

REVERSE_LABEL_MAP = {0: "NORMAL", 1: "SUSPICIOUS", 2: "ATTACK"}


def generate_synthetic_dataset(num_samples: int = 1500, seed: int = 42) -> Tuple[List[SecurityEvent], List[int]]:
    """
    Generates a balanced dataset of SecurityEvent telemetry records using exact Q-Sentinel
    simulation routines across clean runs, noise, forgery, replay, and impersonation.

    Target Classes:
    0: NORMAL (Clean legitimate traffic)
    1: SUSPICIOUS (Low noise, minor deviation)
    2: ATTACK (State forgery, replay, impersonation, severe noise)
    """
    random.seed(seed)
    np.random.seed(seed)

    events: List[SecurityEvent] = []
    labels: List[int] = []

    pauli_list = list(PAULI_STATES.keys())
    bases = ["X", "Y", "Z"]

    per_class = num_samples // 3

    # Helper function to generate single event fast
    def make_event(st_name, basis, shots, atk_type, sev, signer_id, exp_signer, nonce):
        ctx = SessionContext(signer_id=signer_id, expected_signer_id=exp_signer, nonce=nonce)
        cfg = ExperimentConfig(
            input_state=st_name,
            measurement_basis=basis,
            shots=shots,
            attack_type=atk_type,
            attack_severity=sev,
            session_context=ctx
        )
        rec = run_qds_experiment(cfg)
        return SecurityEvent.from_experiment_record(rec)

    # 1. Generate NORMAL samples (Clean traffic)
    for i in range(per_class):
        st_name = pauli_list[i % len(pauli_list)]
        basis = bases[i % len(bases)]
        shots = [500, 1000, 2000, 5000][i % 4]
        evt = make_event(st_name, basis, shots, "none", 0.0, "Alice_PubKey_0x8F4A", "Alice_PubKey_0x8F4A", f"NONCE-{10000+i}")
        events.append(evt)
        labels.append(LABEL_MAP["NORMAL"])

    # 2. Generate SUSPICIOUS samples (Low severity noise λ in [0.05, 0.15])
    for i in range(per_class):
        st_name = pauli_list[i % len(pauli_list)]
        basis = bases[i % len(bases)]
        shots = [500, 1000, 2000][i % 3]
        atk = ["bit_flip", "phase_flip", "depolarizing", "state_forgery"][i % 4]
        sev = round(0.05 + (i % 11) * 0.01, 2)
        evt = make_event(st_name, basis, shots, atk, sev, "Alice_PubKey_0x8F4A", "Alice_PubKey_0x8F4A", f"NONCE-{20000+i}")
        events.append(evt)
        labels.append(LABEL_MAP["SUSPICIOUS"])

    # 3. Generate ATTACK samples (High severity forgery λ >= 0.25, replay, impersonation)
    for i in range(per_class):
        st_name = pauli_list[i % len(pauli_list)]
        basis = bases[i % len(bases)]
        shots = [500, 1000, 2000][i % 3]
        cat = i % 3

        if cat == 0:
            evt = make_event(st_name, basis, shots, "replay", 0.0, "Alice_PubKey_0x8F4A", "Alice_PubKey_0x8F4A", "expired_nonce_999")
        elif cat == 1:
            evt = make_event(st_name, basis, shots, "impersonation", 0.0, "Eve_Mallory_0x999", "Alice_PubKey_0x8F4A", f"NONCE-{30000+i}")
        else:
            atk = ["state_forgery", "depolarizing", "bit_flip", "phase_flip"][i % 4]
            sev = round(0.25 + (i % 55) * 0.01, 2)
            evt = make_event(st_name, basis, shots, atk, sev, "Alice_PubKey_0x8F4A", "Alice_PubKey_0x8F4A", f"NONCE-{40000+i}")

        events.append(evt)
        labels.append(LABEL_MAP["ATTACK"])

    return events, labels
