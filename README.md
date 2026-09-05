# 🛡️ Q-Sentinel: Quantum Cyber Threat Laboratory for Digital Signature Security

[![Problem Statement](https://img.shields.io/badge/SIH-SIH26141-blue)](https://www.sih.gov.in/sih2026PS)
[![Domain](https://img.shields.io/badge/Domain-Blockchain%20%26%20Cybersecurity-purple)](#)
[![Methodology](https://img.shields.io/badge/Detection-Rule--Based%20%2F%20No%20AI%2FML-green)](#)
[![Python](https://img.shields.io/badge/Python-3.11%2B-informational)](#)
[![Framework](https://img.shields.io/badge/UI-Flask%20%2B%20Neo--Brutalism-ff0055)](#)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.x-6100a8)](#)

> **Build Target**: A dual-domain **Quantum Cyber Threat Laboratory** featuring a primary teleportation-based **Quantum Digital Signature (QDS) Security Detector** (SIH26141 core) alongside a **Classical Digital Signature Quantum-Threat Analysis Engine**, **Post-Quantum Signature Benchmarking**, and **Deterministic Quantum Risk Scoring** with **NO AI/ML**.

---

## 🌟 Key Architecture & Capabilities

```
Q-Sentinel System Architecture
│
├── 🛡️ Domain A: Quantum Signature Security (SIH26141 Primary Baseline)
│   ├── QDS Teleportation Engine (3-qubit Bell states |Φ⁺⟩, Pauli projections)
│   ├── Statistical Detector Engine (z-score, Chi-Square test, p-values, empirical calibration)
│   └── Protocol Integrity Verification (State forgery, channel noise, replay & impersonation)
│
├── ⚡ Domain B: Classical Signature Quantum Threat Analysis (Attack Engine)
│   ├── Shor Factorization Lab (Toy integer factorization: N = 15, 21, 35, 77, 91, 143)
│   ├── ECC Discrete Log Lab (Toy curve discrete-log state modeling over GF(p))
│   ├── Grover Search Lab (Quadratic preimage search complexity O(N) vs O(√N))
│   └── CRQC Resource Estimator (Logical qubits, T-depth, surface code physical qubits)
│
├── 📜 Domain C: Post-Quantum Signature (PQC) Analysis
│   ├── NIST PQC Standards (FIPS 204 ML-DSA-44/65/87, FIPS 205 SLH-DSA-128/192/256)
│   └── Public Key & Signature Size Overhead Benchmarking
│
├── 📊 Domain D: Unified Deterministic Risk Assessment
│   ├── Mosca Theorem Migration Horizon Calculation (X + Y > Z)
│   └── Risk Classification (LOW, MODERATE, HIGH, CRITICAL)
│
└── 🎨 Frontend: Flask + Neo-Brutalism & Cinematic Quantum Wave Canvas
```

---

## 🎨 Neo-Brutalism UI & Cinematic Quantum Interface

- **High-Contrast Design System**: Bold 3px solid black borders, hard offset drop shadows (`5px 5px 0px #00f0ff` / `#ff0055` / `#00ff66`), zero border radius cards.
- **Cinematic Canvas Background**: Dynamic HTML5 canvas simulation rendering real-time quantum wave packet superposition and entangled particle networks.
- **Interactive REST APIs**: Flask API-driven dashboard rendering live Chart.js probability distribution updates.

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

### 2. Run Unit Test Suite
```bash
pytest tests/ -v
```
*(All 43 unit tests passing: 25 legacy QDS tests + 18 new quantum attack tests).*

### 3. Run Reproducible Research Experiments
```bash
python experiments/quantum_attacks/shor_rsa_experiment.py
python experiments/quantum_attacks/grover_search_experiment.py
python experiments/quantum_attacks/ecc_dlog_experiment.py
python experiments/quantum_attacks/pqc_benchmark_experiment.py
```

### 4. Launch Flask Neo-Brutalism Security System
```bash
python wsgi.py
```
Open **`http://localhost:5000`** in your browser.

---

## 📂 Repository Structure

```
.
├── wsgi.py                      # Flask server WSGI entrypoint script
├── requirements.txt              # Dependency specification (Qiskit, Flask, Pytest)
├── pyproject.toml               # Package build configuration
├── flask_app/                   # Flask Web Application & Neo-Brutalism UI
│   ├── __init__.py              # App factory
│   ├── routes.py                # Page routes and JSON REST API handlers
│   ├── static/
│   │   ├── css/
│   │   │   └── neo_brutalism.css# Neo-Brutalism design system stylesheet
│   │   └── js/
│   │       └── quantum_canvas.js# Cinematic quantum particle background animation
│   └── templates/               # Jinja2 Neo-Brutalism HTML Templates
│       ├── base.html            # Core layout & sidebar navigation
│       ├── qds_lab.html         # 🛡️ QDS Teleportation Threat Lab (Primary SIH Module)
│       ├── classical_threats.html# ⚡ Classical Signature Threat Matrix Overview
│       ├── shor_lab.html        # 🔢 Shor Factorization Laboratory
│       ├── grover_lab.html      # 🔍 Grover Search Complexity Laboratory
│       ├── pqc_lab.html         # 📜 NIST PQC Comparison Laboratory
│       └── risk_lab.html        # 📊 Unified Quantum Risk Assessment Engine
├── src/
│   └── qds_detector/
│       ├── config.py            # ExperimentConfig, SessionContext, ThresholdConfig
│       ├── states.py            # 6 Pauli basis eigenstates & density matrices
│       ├── bell.py              # Bell pair preparation & measurement
│       ├── teleportation.py     # 3-qubit quantum teleportation pipeline
│       ├── measurements.py      # Pauli projective measurement operators (X, Y, Z)
│       ├── channels.py          # Bit-flip, phase-flip, depolarizing quantum noise
│       ├── attacks.py           # Quantum state forgery & protocol replay/impersonation
│       ├── statistics.py        # z-score, Chi-Square, p-values, probability deviation
│       ├── detector.py          # Deterministic decision rule engine (ACCEPT/SUSPICIOUS/REJECT)
│       ├── metrics.py           # Security metrics (TPR, FPR, FAR, FRR)
│       ├── protocol.py          # End-to-end QDS protocol orchestrator
│       ├── calibration.py       # Empirical threshold calibration
│       ├── reporting.py         # Reproducibility JSON/CSV exporter
│       └── quantum_attacks/     # Classical Signature Quantum Threat Engine
│           ├── shor.py          # Shor's period finding & factorizer
│           ├── ecc_analysis.py  # ECC discrete log attack simulation
│           ├── grover.py        # Grover preimage search analysis
│           ├── resource_estimator.py # CRQC surface code resource estimator
│           ├── pqc_analysis.py  # NIST ML-DSA / SLH-DSA metadata
│           └── quantum_risk.py  # Deterministic risk classification engine
├── experiments/                 # Research experiment suite & JSON result outputs
├── tests/                       # Automated unit test suite (43 passing tests)
└── docs/                        # Technical architecture & threat model documentation
```

---

## 🔬 Scientific Limitations & Guardrails

> [!IMPORTANT]
> **Scientific Integrity Standard**:
> 1. Interactive classical cryptanalysis (Shor, ECC discrete log) operates strictly on **educational toy-scale parameters** ($N \in \{15, 21, 35, 77\}$ or small prime fields $\mathbb{F}_p$).
> 2. Real-world parameter evaluations (e.g., RSA-2048 or ECDSA P-256) are calculated via a dedicated **fault-tolerant CRQC surface code resource estimation model**.
> 3. Zero AI/ML models are used across any detection or risk engine; all decisions rely on transparent deterministic mathematical rules and hypothesis testing.
> 4. PQC standards (ML-DSA / SLH-DSA) are described as *"designed to resist known classical and quantum attack strategies"* without claiming unbacked absolute mathematical proof.

---

## 📜 References & Standards
1. Smart India Hackathon 2026, Problem Statement SIH26141, Egreen Quanta.
2. NIST FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA), 2024.
3. NIST FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA), 2024.
4. Gidney, C., & Ekerå, M. (2021). How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits. *Quantum*, 5, 433.
