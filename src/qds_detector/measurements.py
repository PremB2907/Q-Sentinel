"""
Projective Measurement Utilities for Pauli Observables (X, Y, Z).

Computes projective measurement outcome probabilities P+ = (I + sigma)/2 and P- = (I - sigma)/2
for both statevectors and density matrices.
"""

import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, Operator

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

PAULI_MATRICES = {"X": X, "Y": Y, "Z": Z}


def get_projectors(basis: str) -> tuple[np.ndarray, np.ndarray]:
    """Return positive P+ and negative P- projectors for given Pauli basis (X, Y, or Z)."""
    b = basis.upper()
    if b not in PAULI_MATRICES:
        raise ValueError(f"Invalid basis '{basis}'. Must be X, Y, or Z.")
    sigma = PAULI_MATRICES[b]
    P_plus = 0.5 * (I + sigma)
    P_minus = 0.5 * (I - sigma)
    return P_plus, P_minus


def evaluate_state_projective_probabilities(
    state: Statevector | DensityMatrix,
    basis: str
) -> dict[str, float]:
    """
    Evaluate exact quantum mechanics outcome probabilities p+ and p- for state under Pauli basis measurement.
    p_plus = Tr(P_plus * rho)
    p_minus = Tr(P_minus * rho)
    """
    P_plus, P_minus = get_projectors(basis)
    
    if isinstance(state, Statevector):
        rho = DensityMatrix(state).data
    elif isinstance(state, DensityMatrix):
        rho = state.data
    else:
        rho = np.array(state, dtype=complex)
        
    p_plus = float(np.real(np.trace(P_plus @ rho)))
    p_minus = float(np.real(np.trace(P_minus @ rho)))
    
    # Clip values to ensure proper probability bounds [0.0, 1.0]
    p_plus = max(0.0, min(1.0, p_plus))
    p_minus = max(0.0, min(1.0, p_minus))
    
    return {"+1": p_plus, "-1": p_minus}


def normalize_counts(counts: dict[str, int], shots: int) -> dict[str, float]:
    """Normalize count dictionary into probability dictionary."""
    total = sum(counts.values()) if sum(counts.values()) > 0 else shots
    return {k: v / total for k, v in counts.items()}
