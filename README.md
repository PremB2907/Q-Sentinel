# Q-Sentinel: Quantum-Inspired Cyber Threat Detection for Digital Signature Security

[![Problem Statement](https://img.shields.io/badge/SIH-SIH26141-blue)](https://www.sih.gov.in/sih2026PS)
[![Domain](https://img.shields.io/badge/Domain-Blockchain%20%26%20Cybersecurity-purple)](#)
[![Methodology](https://img.shields.io/badge/Detection-Rule--Based%20%2F%20No%20AI%2FML-green)](#)
[![Python](https://img.shields.io/badge/Python-3.11%2B-informational)](#)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.x-6100a8)](#)

> **Build Target**: A fully simulated teleportation-based Quantum Digital Signature (QDS) threat-detection prototype using quantum measurement statistics and deterministic threshold rules, with **NO AI/ML**.

---

## 🌟 Key Features

- **Quantum Core**:
  - 6 Pauli eigenstates ($|0\rangle, |1\rangle, |+\rangle, |-\rangle, |+i\rangle, |-i\rangle$).
  - Entangled Bell pair preparation ($|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$).
  - 3-qubit quantum teleportation circuit with classical Bell outcome corrections ($I, X, Z, ZX$).
  - Pauli basis projective measurements ($P_\pm = \frac{I \pm \sigma}{2}$).
- **Threat Engine**:
  - **State Forgery**: State perturbation mixture model $\rho_{\text{attack}} = (1-\lambda)\rho_{\text{legit}} + \lambda \rho_{\text{forge}}$.
  - **Channel Manipulation**: Bit-flip, phase-flip, and depolarizing noise channels.
  - **Replay Attack**: Protocol-layer session transcript reuse with expired nonces.
  - **Impersonation Attack**: Protocol-layer context mismatch (wrong signer identity).
- **Rule-Based Threat Detector**:
  - Deterministic evaluation using Binomial Standard Error, $z$-score, Chi-Square test, $p$-value, fidelity $F$, and protocol context.
  - 3-state decision engine: **ACCEPT**, **SUSPICIOUS**, **REJECT**.
  - **Strictly zero AI/ML algorithms** as required by SIH26141 problem statement.
- **Interactive Security Laboratory Dashboard**:
  - Streamlit UI with live quantum teleportation state display, distribution charts, threat decision callout badges, and attack severity ($\lambda$) sensitivity sweeps.

---

## 🛠️ Quick Start

### 1. Environment Setup
```bash
# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and package in editable mode
pip install -r requirements.txt
pip install -e .
```

### 2. Run Test Suite
```bash
pytest tests/ -v
```

### 3. Launch Streamlit Laboratory Dashboard
```bash
streamlit run app.py
```

---

## 📂 Repository Structure

```
.
├── app.py                      # Streamlit interactive security laboratory UI
├── pyproject.toml              # Python build & dependency metadata
├── requirements.txt            # Dependency list
├── src/
│   └── qds_detector/
│       ├── config.py           # Dataclasses for thresholds, context, and configs
│       ├── states.py           # 6 Pauli basis eigenstates & density matrices
│       ├── bell.py             # Bell pair preparation & measurement
│       ├── teleportation.py    # 3-qubit quantum teleportation pipeline
│       ├── measurements.py     # Pauli projective measurements (X, Y, Z)
│       ├── channels.py         # Quantum noise channels (bit-flip, phase-flip, depolarizing)
│       ├── attacks.py          # Threat simulation engine (forgery, channel, replay, impersonation)
│       ├── statistics.py       # z-scores, chi-square, confidence bounds, probability deviation
│       ├── detector.py         # Deterministic decision engine (NO AI/ML!)
│       ├── metrics.py          # Security evaluation metrics (TPR, FPR, FAR, FRR)
│       ├── protocol.py         # End-to-end protocol orchestrator
│       └── reporting.py        # Reproducibility JSON/CSV exporter
├── tests/                      # Automated unit test suite (25 tests)
├── docs/                       # Technical architecture & protocol documentation
└── SIH26141_...docx            # Engineering implementation blueprint
```

---

## 🔬 Research & Reference Standards
1. Smart India Hackathon 2026, Problem Statement SIH26141, Egreen Quanta.
2. Teleportation-based continuous-variable quantum digital signature, *Reports in Physics*, 2023.
3. Optimal verification of Bell and GHZ states in untrusted quantum networks, *npj Quantum Information*.
