"""
Shor's Algorithm Toy Factorization & Quantum Period-Finding Simulation.
SIH26141 • Egreen Quanta

Demonstrates quantum integer factorization mechanics for toy semiprimes (e.g. N = 15, 21, 35, 77).
Exposes period finding: N -> Base a -> Period r -> gcd(a^(r/2) ± 1, N) -> Factors.
"""

import math
import time
from typing import Dict, Any, List, Optional, Tuple


SUPPORTED_SEMIPRIMES: Dict[int, List[int]] = {
    15: [3, 5],
    21: [3, 7],
    35: [5, 7],
    77: [7, 11],
    91: [7, 13],
    143: [11, 13],
}


def find_period_classical(a: int, N: int) -> int:
    """Find order/period r of a modulo N classically: f(x) = a^x mod N = 1."""
    if math.gcd(a, N) != 1:
        return 0
    r = 1
    val = (a % N)
    while val != 1 and r <= N:
        val = (val * a) % N
        r += 1
    return r if val == 1 else 0


def run_shor_factorization(
    N: int = 15,
    base_a: Optional[int] = None,
    seed: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Simulates Shor's algorithm for factorizing a toy semiprime integer N.

    Args:
        N: Semiprime integer to factorize (e.g., 15, 21, 35, 77).
        base_a: Coprime base a < N. If None, automatically selects a valid base.
        seed: Random seed for deterministic selection if needed.

    Returns:
        Dictionary containing execution trace, period r, recovered factors,
        simulated qubit count, and performance runtime.
    """
    start_time = time.perf_counter()
    
    if N not in SUPPORTED_SEMIPRIMES:
        # Check if even or trivial factor
        if N % 2 == 0:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "algorithm": "RSA-Shor",
                "modulus_N": N,
                "base_a": 2,
                "period_r": None,
                "factors": [2, N // 2],
                "successful": True,
                "mode": "classical_trivial_check",
                "qubit_count": 0,
                "attempts": 1,
                "runtime_ms": round(elapsed, 3),
                "notes": "Modulus is even; trivial factor 2 recovered classically.",
            }

    # Step 1: Base selection
    valid_bases = [a for a in range(2, N) if math.gcd(a, N) == 1]
    if not valid_bases:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "algorithm": "RSA-Shor",
            "modulus_N": N,
            "base_a": None,
            "period_r": None,
            "factors": [],
            "successful": False,
            "mode": "toy_simulation",
            "qubit_count": 0,
            "attempts": 0,
            "runtime_ms": round(elapsed, 3),
            "notes": "No valid coprime base found.",
        }

    if base_a is None or base_a not in valid_bases:
        # Pick default base tailored for smooth demonstration
        default_bases = {15: 7, 21: 2, 35: 3, 77: 2, 91: 3, 143: 2}
        base_a = default_bases.get(N, valid_bases[0])

    # Step 2: Check if gcd(a, N) > 1 gives non-trivial factor directly
    g = math.gcd(base_a, N)
    if g > 1:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "algorithm": "RSA-Shor",
            "modulus_N": N,
            "base_a": base_a,
            "period_r": None,
            "factors": sorted([g, N // g]),
            "successful": True,
            "mode": "classical_gcd_hit",
            "qubit_count": math.ceil(2 * math.log2(N)) + 3,
            "attempts": 1,
            "runtime_ms": round(elapsed, 3),
            "notes": f"Direct classical GCD hit: gcd({base_a}, {N}) = {g}.",
        }

    # Step 3: Simulated Quantum Period Finding
    period_r = find_period_classical(base_a, N)
    
    # Estimate required logical qubits: 2n + 3 where n = log2(N)
    n_bits = math.ceil(math.log2(N))
    simulated_qubits = 2 * n_bits + 3

    # Step 4: Extract factors from period r
    successful = False
    factors: List[int] = []
    
    if period_r > 0 and period_r % 2 == 0:
        half_power = pow(base_a, period_r // 2, N)
        if half_power != (N - 1):  # half_power != -1 mod N
            f1 = math.gcd(half_power - 1, N)
            f2 = math.gcd(half_power + 1, N)
            candidates = [f for f in (f1, f2) if 1 < f < N]
            if candidates:
                p = candidates[0]
                q = N // p
                factors = sorted([p, q])
                successful = True

    elapsed = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "RSA-Shor",
        "modulus_N": N,
        "base_a": base_a,
        "period_r": period_r,
        "factors": factors if successful else [],
        "successful": successful,
        "mode": "toy_simulation",
        "qubit_count": simulated_qubits,
        "attempts": 1,
        "runtime_ms": round(elapsed, 3),
        "execution_steps": [
            f"Modulus N = {N} (bit length = {n_bits})",
            f"Selected base a = {base_a} with gcd({base_a}, {N}) = 1",
            f"Simulated Quantum Phase Estimation (QPE) -> Period r = {period_r}",
            f"Checked parity: r = {period_r} is {'even' if period_r % 2 == 0 else 'odd'}",
            f"Evaluated a^(r/2) mod N = {pow(base_a, period_r // 2, N) if period_r % 2 == 0 else 'N/A'}",
            f"GCD Extraction: gcd({base_a}^({period_r // 2 if period_r % 2 == 0 else 0}) - 1, {N}) and gcd(+1)",
            f"Factorization Outcome: {factors if successful else 'Failed to split'}"
        ],
        "notes": "Toy-scale simulation of Shor's algorithm for quantum risk education.",
    }
