"""
Grover's Quantum Search Algorithm Analysis & Preimage Oracle Simulation.
SIH26141 • Egreen Quanta

Demonstrates Grover's quadratic search speedup O(N) -> O(sqrt(N)).
Analyzes cryptographic search implications on symmetric keys and hash-based signatures.
"""

import math
import time
from typing import Dict, Any, List, Optional


def run_grover_search_analysis(
    key_space_bits: int = 8,
    target_index: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulates Grover's algorithm search iteration count and probability amplification
    for a toy key space of size N = 2^key_space_bits.

    Args:
        key_space_bits: Bit length of search space (e.g. 4 to 12 bits for simulation).
        target_index: Integer secret index to find. Defaults to midpoint.

    Returns:
        Dictionary containing classical vs Grover search iterations, success probability,
        simulated qubit count, iteration step metrics, and cryptographic implications.
    """
    start_time = time.perf_counter()

    N = 1 << key_space_bits  # Search space size 2^k
    if target_index is None or not (0 <= target_index < N):
        target_index = N // 2

    # Classical linear search metrics
    classical_avg_attempts = N / 2.0
    classical_worst_attempts = N

    # Grover search metrics
    # Optimal iterations M = floor(pi / 4 * sqrt(N))
    grover_iterations = max(1, int(math.floor((math.pi / 4.0) * math.sqrt(N))))
    
    # Calculate Grover amplitude amplification trace
    # Initial uniform superposition amplitude a0 = 1 / sqrt(N)
    theta = math.asin(1.0 / math.sqrt(N))
    
    amplitude_trace: List[Dict[str, float]] = []
    for step in range(grover_iterations + 1):
        angle = (2 * step + 1) * theta
        target_prob = math.sin(angle) ** 2
        amplitude_trace.append({
            "iteration": step,
            "target_probability": round(target_prob, 6),
            "other_probability": round((1.0 - target_prob) / (N - 1) if N > 1 else 0.0, 6)
        })

    final_success_prob = amplitude_trace[-1]["target_probability"]
    speedup_factor = round(classical_avg_attempts / grover_iterations, 2)

    elapsed = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Grover-Search",
        "key_space_bits": key_space_bits,
        "search_space_size_N": N,
        "target_index": target_index,
        "classical_avg_attempts": classical_avg_attempts,
        "classical_worst_attempts": classical_worst_attempts,
        "grover_iterations": grover_iterations,
        "grover_final_success_probability": final_success_prob,
        "speedup_factor": speedup_factor,
        "qubit_count": key_space_bits + 1,  # k qubits for index + 1 ancilla for oracle
        "amplitude_trace": amplitude_trace,
        "runtime_ms": round(elapsed, 3),
        "cryptographic_implications": {
            "AES_128": "Effective quantum security reduced to ~64 bits (O(2^64) operations).",
            "AES_256": "Effective quantum security reduced to ~128 bits (Remains secure).",
            "Hash_Preimage": "Preimage security halved from 2^b to 2^(b/2).",
            "Digital_Signatures": "Grover provides quadratic preimage speedup, but does NOT instantly break asymmetric signature math like Shor does."
        },
        "notes": "Toy Grover search demonstration illustrating quadratic amplitude amplification."
    }
