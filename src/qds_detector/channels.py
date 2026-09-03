"""
Quantum Noise Channel Models for Channel Manipulation Attacks.

Implements mathematical quantum channels operating on density matrices:
- Bit-flip channel: rho -> (1-p)*rho + p * X * rho * X
- Phase-flip channel: rho -> (1-p)*rho + p * Z * rho * Z
- Bit-phase-flip channel: rho -> (1-p)*rho + p * Y * rho * Y
- Depolarizing channel: rho -> (1-p)*rho + (p/3) * (X*rho*X + Y*rho*Y + Z*rho*Z)
"""

import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector
from qds_detector.measurements import X, Y, Z, I


def apply_bit_flip_channel(state: Statevector | DensityMatrix, p: float) -> DensityMatrix:
    """Apply bit-flip channel with noise probability p in [0, 1]."""
    p = max(0.0, min(1.0, float(p)))
    rho = DensityMatrix(state).data
    rho_noisy = (1.0 - p) * rho + p * (X @ rho @ X)
    return DensityMatrix(rho_noisy)


def apply_phase_flip_channel(state: Statevector | DensityMatrix, p: float) -> DensityMatrix:
    """Apply phase-flip channel with noise probability p in [0, 1]."""
    p = max(0.0, min(1.0, float(p)))
    rho = DensityMatrix(state).data
    rho_noisy = (1.0 - p) * rho + p * (Z @ rho @ Z)
    return DensityMatrix(rho_noisy)


def apply_bit_phase_flip_channel(state: Statevector | DensityMatrix, p: float) -> DensityMatrix:
    """Apply bit-phase-flip channel with noise probability p in [0, 1]."""
    p = max(0.0, min(1.0, float(p)))
    rho = DensityMatrix(state).data
    rho_noisy = (1.0 - p) * rho + p * (Y @ rho @ Y)
    return DensityMatrix(rho_noisy)


def apply_depolarizing_channel(state: Statevector | DensityMatrix, p: float) -> DensityMatrix:
    """Apply single-qubit depolarizing channel with noise probability p in [0, 1]."""
    p = max(0.0, min(1.0, float(p)))
    rho = DensityMatrix(state).data
    term_x = X @ rho @ X
    term_y = Y @ rho @ Y
    term_z = Z @ rho @ Z
    rho_noisy = (1.0 - p) * rho + (p / 3.0) * (term_x + term_y + term_z)
    return DensityMatrix(rho_noisy)
