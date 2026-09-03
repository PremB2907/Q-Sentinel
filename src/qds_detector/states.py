"""
Pauli Eigenstates & Density Matrix Utilities for QDS Protocol.

Defines the six Pauli basis eigenstates:
- Z-basis: |0>, |1>
- X-basis: |+>, |->
- Y-basis: |+i>, |-i>
"""

import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity


PAULI_STATES = {
    "|0>": np.array([1.0, 0.0], dtype=complex),
    "|1>": np.array([0.0, 1.0], dtype=complex),
    "|+>": np.array([1.0, 1.0], dtype=complex) / np.sqrt(2),
    "|->": np.array([1.0, -1.0], dtype=complex) / np.sqrt(2),
    "|+i>": np.array([1.0, 1j], dtype=complex) / np.sqrt(2),
    "|-i>": np.array([1.0, -1j], dtype=complex) / np.sqrt(2),
}

# Mapping short strings to full names
STATE_ALIASES = {
    "0": "|0>", "|0>": "|0>",
    "1": "|1>", "|1>": "|1>",
    "+": "|+>", "|+>": "|+>",
    "-": "|->", "|->": "|->",
    "+i": "|+i>", "|+i>": "|+i>",
    "-i": "|-i>", "|-i>": "|-i>",
}


def get_statevector(state_name: str) -> Statevector:
    """Return Qiskit Statevector for given state name or alias."""
    name = STATE_ALIASES.get(state_name, state_name)
    if name not in PAULI_STATES:
        raise ValueError(f"Unknown state '{state_name}'. Valid states: {list(PAULI_STATES.keys())}")
    return Statevector(PAULI_STATES[name])


def get_density_matrix(state_name: str) -> DensityMatrix:
    """Return Qiskit DensityMatrix for pure state."""
    sv = get_statevector(state_name)
    return DensityMatrix(sv)


def calculate_fidelity(state_a: Statevector | DensityMatrix, state_b: Statevector | DensityMatrix) -> float:
    """Calculate quantum state fidelity F(rho, sigma) in range [0, 1]."""
    fidelity = state_fidelity(state_a, state_b)
    return float(np.real(fidelity))


def get_expected_probabilities(state_name: str, basis: str) -> dict[str, float]:
    """
    Return theoretical outcome probabilities for measuring state_name in specified basis.
    Outcome keys: '+1' and '-1'.
    """
    name = STATE_ALIASES.get(state_name, state_name)
    basis = basis.upper()
    
    # Projective measurement expected results
    if basis == "Z":
        if name == "|0>":
            return {"+1": 1.0, "-1": 0.0}
        elif name == "|1>":
            return {"+1": 0.0, "-1": 1.0}
        else:
            return {"+1": 0.5, "-1": 0.5}
            
    elif basis == "X":
        if name == "|+>":
            return {"+1": 1.0, "-1": 0.0}
        elif name == "|->":
            return {"+1": 0.0, "-1": 1.0}
        else:
            return {"+1": 0.5, "-1": 0.5}
            
    elif basis == "Y":
        if name == "|+i>":
            return {"+1": 1.0, "-1": 0.0}
        elif name == "|-i>":
            return {"+1": 0.0, "-1": 1.0}
        else:
            return {"+1": 0.5, "-1": 0.5}
            
    else:
        raise ValueError(f"Unsupported measurement basis '{basis}'. Must be X, Y, or Z.")
