"""
Unit tests for Bell state preparation and measurement.
"""

import pytest
import numpy as np
from qiskit_aer import AerSimulator
from qds_detector.bell import create_bell_pair


def test_bell_pair_preparation():
    """Verify |Phi+> state preparation produces ~50% '00' and ~50% '11' in Z basis."""
    qc = create_bell_pair()
    qc.measure_all()
    
    sim = AerSimulator()
    job = sim.run(qc, shots=5000, seed_simulator=42)
    counts = job.result().get_counts()
    
    # Bell state |Phi+> should only have outcomes 00 and 11
    assert "01" not in counts or counts["01"] == 0
    assert "10" not in counts or counts["10"] == 0
    
    p00 = counts.get("00", 0) / 5000
    p11 = counts.get("11", 0) / 5000
    
    assert pytest.approx(p00, abs=0.05) == 0.5
    assert pytest.approx(p11, abs=0.05) == 0.5
