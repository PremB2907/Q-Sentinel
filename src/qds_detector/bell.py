"""
Bell State Preparation & Bell Measurement Utilities.

Implements standard Bell pair preparation |Phi+> = (|00> + |11>) / sqrt(2)
and Bell basis measurements for quantum teleportation.
"""

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.quantum_info import Statevector


def create_bell_pair() -> QuantumCircuit:
    """
    Create a 2-qubit circuit that prepares the maximally entangled Bell state |Phi+>.
    Qubit 0: Sender Bell qubit (B)
    Qubit 1: Receiver Bell qubit (C)
    """
    qc = QuantumCircuit(2, name="|Phi+>")
    qc.h(0)
    qc.cx(0, 1)
    return qc


def apply_bell_measurement(qc: QuantumCircuit, qubit_a: int, qubit_b: int, clbit_a: int, clbit_b: int) -> None:
    """
    Apply Bell basis measurement on qubit_a (state qubit) and qubit_b (sender Bell qubit).
    
    Operations:
    1. CNOT(qubit_a, qubit_b)
    2. H(qubit_a)
    3. Measure qubit_a -> clbit_a
    4. Measure qubit_b -> clbit_b
    """
    qc.cx(qubit_a, qubit_b)
    qc.h(qubit_a)
    qc.measure(qubit_a, clbit_a)
    qc.measure(qubit_b, clbit_b)
