"""
3-Qubit Quantum Teleportation Circuit with Classical Bell Measurement & Pauli Corrections.
"""

from typing import Dict, Any, Tuple
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

from qds_detector.states import get_statevector, get_expected_probabilities, STATE_ALIASES
from qds_detector.bell import apply_bell_measurement


def build_teleportation_circuit(
    input_state_name: str,
    measurement_basis: str = "Z"
) -> QuantumCircuit:
    """
    Build a full 3-qubit quantum teleportation circuit with Pauli corrections and projective measurement.
    
    Qubit 0: Test state qubit (A)
    Qubit 1: Sender entangled qubit (B)
    Qubit 2: Receiver entangled qubit (C)
    
    Classical Register 0 (c_bell): 2 bits for Bell measurement (clbit 0: q0, clbit 1: q1)
    Classical Register 1 (c_target): 1 bit for receiver measurement (clbit 0: q2)
    """
    qspec = QuantumRegister(3, "q")
    c_bell = ClassicalRegister(2, "c_bell")
    c_target = ClassicalRegister(1, "c_target")
    
    qc = QuantumCircuit(qspec, c_bell, c_target, name=f"Teleportation({input_state_name})")
    
    # 1. Initialize input state on qubit 0
    sv = get_statevector(input_state_name)
    qc.initialize(sv, 0)
    qc.barrier()
    
    # 2. Prepare Bell pair |Phi+> on qubits 1 and 2
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    
    # 3. Bell measurement on qubits 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, c_bell[0])
    qc.measure(1, c_bell[1])
    qc.barrier()
    
    # 4. Pauli corrections on receiver qubit 2 conditioned on Bell measurement outcomes
    # Bit flip X if qubit 1 measured 1 (c_bell[1])
    with qc.if_test((c_bell[1], 1)):
        qc.x(2)
        
    # Phase flip Z if qubit 0 measured 1 (c_bell[0])
    with qc.if_test((c_bell[0], 1)):
        qc.z(2)
        
    qc.barrier()
    
    # 5. Basis change for projective measurement on receiver qubit 2
    basis = measurement_basis.upper()
    if basis == "Z":
        # Computational basis: direct Z measurement
        pass
    elif basis == "X":
        # Hadamard basis: H -> measure Z
        qc.h(2)
    elif basis == "Y":
        # Phase basis: Sdg -> H -> measure Z
        qc.sdg(2)
        qc.h(2)
    else:
        raise ValueError(f"Invalid measurement basis '{basis}'. Must be X, Y, or Z.")
        
    qc.measure(2, c_target[0])
    return qc


def run_teleportation_experiment(
    input_state: str,
    measurement_basis: str = "Z",
    shots: int = 5000,
    seed: int | None = 42
) -> Dict[str, Any]:
    """
    Run clean quantum teleportation simulation using Qiskit Aer backend.
    Returns counts, probabilities, and Bell measurement breakdown.
    """
    state_name = STATE_ALIASES.get(input_state, input_state)
    circuit = build_teleportation_circuit(state_name, measurement_basis)
    
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=shots, seed_simulator=seed)
    result = job.result()
    raw_counts = result.get_counts()
    
    # Parse raw counts (Qiskit formats bitstring as "c_target c_bell", e.g., "0 01")
    target_counts = {"0": 0, "1": 0}
    bell_counts = {"00": 0, "01": 0, "10": 0, "11": 0}
    
    for bitstring, count in raw_counts.items():
        parts = bitstring.split()
        if len(parts) == 2:
            t_bit = parts[0]
            b_bits = parts[1]
        else:
            # Single string formatted as "t b1 b0"
            t_bit = bitstring[0]
            b_bits = bitstring[1:]
            
        target_counts[t_bit] = target_counts.get(t_bit, 0) + count
        if b_bits in bell_counts:
            bell_counts[b_bits] += count

    # Map target bit 0 -> outcome '+1' and bit 1 -> outcome '-1'
    outcome_counts = {
        "+1": target_counts.get("0", 0),
        "-1": target_counts.get("1", 0)
    }
    
    total_shots = sum(outcome_counts.values())
    observed_probabilities = {
        "+1": outcome_counts["+1"] / total_shots,
        "-1": outcome_counts["-1"] / total_shots
    }
    
    expected_probabilities = get_expected_probabilities(state_name, measurement_basis)
    
    return {
        "input_state": state_name,
        "measurement_basis": measurement_basis,
        "shots": shots,
        "seed": seed,
        "counts": outcome_counts,
        "observed_probabilities": observed_probabilities,
        "expected_probabilities": expected_probabilities,
        "bell_counts": bell_counts,
        "circuit": circuit
    }
