# Q-Sentinel: Quantum Cyber Threat Laboratory for Digital Signature Security

[![Problem Statement](https://img.shields.io/badge/SIH-SIH26141-blue)](https://www.sih.gov.in/sih2026PS)
[![Domain](https://img.shields.io/badge/Domain-Blockchain%20%26%20Cybersecurity-purple)](#)
[![Methodology](https://img.shields.io/badge/Detection-Rule--Based%20%2F%20No%20AI%2FML-green)](#)
[![Python](https://img.shields.io/badge/Python-3.11%2B-informational)](#)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.x-6100a8)](#)

> **Build Target**: A dual-domain Quantum Cyber Threat Laboratory combining a **teleportation-based Quantum Digital Signature (QDS) security detector** (SIH26141 core) and a **Classical Digital Signature Quantum-Threat Analysis Laboratory** with deterministic risk scoring and **NO AI/ML**.

---

## 🌟 Architecture & Key Domains

```
Q-Sentinel Architecture
│
├── 🛡️ Domain A: Quantum Signature Security (SIH26141 Primary Core)
│   ├── QDS Teleportation Engine (3-qubit Bell states, Pauli projections)
│   ├── Statistical Detector (z-score, Chi-Square, p-values, empirical calibration)
│   └── Protocol Integrity Engine (State forgery, channel noise, replay & impersonation)
│
├── ⚡ Domain B: Classical Signature Quantum Threat Analysis (Attack Engine)
│   ├── Shor Factorization Lab (Toy integer factorization: N = 15, 21, 35, 77)
│   ├── ECC Discrete Log Lab (Toy curve discrete log state modeling over GF(p))
│   ├── Grover Search Lab (Quadratic preimage search complexity O(N) vs O(sqrt(N)))
│   └── CRQC Resource Estimator (Logical qubits, T-depth, physical surface code qubits)
│
├── 📜 Domain C: Post-Quantum Signature (PQC) Analysis
│   ├── NIST PQC Standards (ML-DSA-44/65/87, SLH-DSA-128/192/256)
│   └── Key & Signature Size Overhead Benchmarking
│
└── 📊 Unified Quantum Risk Assessment Engine
    ├── Deterministic Rule Engine (No AI/ML)
    └── Mosca Theorem Migration Classification (LOW, MODERATE, HIGH, CRITICAL)
```

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

### 2. Run Comprehensive Test Suite
```bash
pytest tests/ -v
```

### 3. Run Reproducible Research Experiments
```bash
python experiments/quantum_attacks/shor_rsa_experiment.py
python experiments/quantum_attacks/grover_search_experiment.py
python experiments/quantum_attacks/ecc_dlog_experiment.py
python experiments/quantum_attacks/pqc_benchmark_experiment.py
```

### 4. Launch Security Laboratory Dashboard
```bash
streamlit run app.py
```

---

## 📂 Repository Structure

```
.
├── app.py                      # Multi-tab Streamlit interactive security laboratory UI
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
│       ├── calibration.py      # Empirical threshold calibration
│       ├── reporting.py        # Reproducibility JSON/CSV exporter
│       └── quantum_attacks/    # [NEW] Classical Signature Quantum Threat Engine
│           ├── shor.py         # Shor's algorithm & period finding
│           ├── ecc_analysis.py # ECC discrete log attack simulation
│           ├── grover.py       # Grover preimage search analysis
│           ├── resource_estimator.py # CRQC surface code resource estimator
│           ├── pqc_analysis.py # NIST ML-DSA / SLH-DSA metadata
│           └── quantum_risk.py # Deterministic risk classification engine
├── experiments/                # Research experiment suite (QDS & Quantum Attacks)
├── tests/                      # Automated unit test suite (43 passing tests)
└── docs/                       # Technical architecture & protocol documentation
```

---

## 🔬 Research & Reference Standards
1. Smart India Hackathon 2026, Problem Statement SIH26141, Egreen Quanta.
2. NIST FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA), 2024.
3. NIST FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA), 2024.
4. Gidney, C., & Ekerå, M. (2021). How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits. *Quantum*, 5, 433.
