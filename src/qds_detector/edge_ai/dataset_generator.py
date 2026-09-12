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


def generate_synthetic_dataset(num_samples: int = 600, seed: int = 42) -> Tuple[List[SecurityEvent], List[int]]:
    """
    Generates balanced dataset of SecurityEvent telemetry records using exact Q-Sentinel
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

    # 1. Generate NORMAL samples
    for _ in range(num_samples // 3):
        st_name = random.choice(pauli_list)
        basis = random.choice(bases)
        shots = random.choice([500, 1000, 2000, 5000])

        ctx = SessionContext(
            signer_id="Alice_PubKey_0x8F4A",
            expected_signer_id="Alice_PubKey_0x8F4A",
            nonce=f"NONCE-{random.randint(1000, 9999)}"
        )
        cfg = ExperimentConfig(
            input_state=st_name,
            measurement_basis=basis,
            shots=shots,
            attack_type="none",
            attack_severity=0.0,
            session_context=ctx
        )
        rec = run_qds_experiment(cfg)
        evt = SecurityEvent.from_experiment_record(rec)
        events.append(evt)
        labels.append(LABEL_MAP["NORMAL"])

    # 2. Generate SUSPICIOUS samples (Low severity noise λ in [0.05, 0.15])
    for _ in range(num_samples // 3):
        st_name = random.choice(pauli_list)
        basis = random.choice(bases)
        shots = random.choice([500, 1000, 2000])
        atk = random.choice(["bit_flip", "phase_flip", "depolarizing", "state_forgery"])
        sev = round(random.uniform(0.05, 0.15), 2)

        ctx = SessionContext(
            signer_id="Alice_PubKey_0x8F4A",
            expected_signer_id="Alice_PubKey_0x8F4A",
            nonce=f"NONCE-{random.randint(1000, 9999)}"
        )
        cfg = ExperimentConfig(
            input_state=st_name,
            measurement_basis=basis,
            shots=shots,
            attack_type=atk,
            attack_severity=sev,
            session_context=ctx
        )
        rec = run_qds_experiment(cfg)
        evt = SecurityEvent.from_experiment_record(rec)
        events.append(evt)
        labels.append(LABEL_MAP["SUSPICIOUS"])

    # 3. Generate ATTACK samples (High severity forgery λ >= 0.25, replay, impersonation)
    for _ in range(num_samples // 3):
        st_name = random.choice(pauli_list)
        basis = random.choice(bases)
        shots = random.choice([500, 1000, 2000])
        atk_category = random.choice(["protocol_replay", "protocol_impersonation", "severe_quantum_attack"])

        if atk_category == "protocol_replay":
            ctx = SessionContext(signer_id="Alice_PubKey_0x8F4A", expected_signer_id="Alice_PubKey_0x8F4A")
            cfg = ExperimentConfig(input_state=st_name, measurement_basis=basis, shots=shots, attack_type="replay", session_context=ctx)
        elif atk_category == "protocol_impersonation":
            ctx = SessionContext(signer_id="Eve_Mallory_0x999", expected_signer_id="Alice_PubKey_0x8F4A")
            cfg = ExperimentConfig(input_state=st_name, measurement_basis=basis, shots=shots, attack_type="impersonation", session_context=ctx)
        else:
            atk = random.choice(["state_forgery", "depolarizing", "bit_flip", "phase_flip"])
            sev = round(random.uniform(0.25, 0.80), 2)
            ctx = SessionContext(signer_id="Alice_PubKey_0x8F4A", expected_signer_id="Alice_PubKey_0x8F4A")
            cfg = ExperimentConfig(input_state=st_name, measurement_basis=basis, shots=shots, attack_type=atk, attack_severity=sev, session_context=ctx)

        rec = run_qds_experiment(cfg)
        evt = SecurityEvent.from_experiment_record(rec)
        events.append(evt)
        labels.append(LABEL_MAP["ATTACK"])

    return events, labels
