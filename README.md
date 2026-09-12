# 🛡️ Q-Sentinel Edge: Privacy-Preserving On-Device Quantum Security Intelligence for Snapdragon-Powered HP PCs

[![Qualcomm Snapdragon AI Lab](https://img.shields.io/badge/Qualcomm-Snapdragon%C2%AE%20AI%20Lab-ff0055)](https://github.com/PremB2907/Q-Sentinel)
[![Problem Statement](https://img.shields.io/badge/SIH-SIH26141-blue)](https://www.sih.gov.in/sih2026PS)
[![Methodology](https://img.shields.io/badge/Authoritative%20Verifier-Deterministic%20%2F%20No%20AI%2FML-green)](#)
[![Edge AI](https://img.shields.io/badge/Edge%20AI-ONNX%20%2F%20QNN%20NPU-00f0ff)](#)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local%20On--Device-yellow)](#)

> **Challenge Submission**: Developed for the **Snapdragon® AI Lab Build & Present Challenge by Qualcomm**, targeting **Snapdragon-powered HP PCs**. Combining a deterministic continuous continuous-variable teleportation Quantum Digital Signature (QDS) detector with an on-device ONNX / Qualcomm QNN local AI intelligence layer.

---

## 🌟 Architectural Principle: AI Advises, Math Verifies

```
Q-Sentinel Edge Dual-Tier Security Architecture
│
├── 🛡️ Authoritative Cryptographic Core (SIH26141 Baseline - 100% Deterministic)
│   ├── QDS Teleportation Engine (3-qubit Bell states |Φ⁺⟩, Pauli projections)
│   ├── Statistical Detector Engine (z-score, Chi-Square test, p-values, empirical calibration)
│   └── Protocol Integrity Engine (State forgery, channel noise, replay & impersonation)
│
├── ⚡ On-Device Edge AI Intelligence Layer (Local ONNX / Qualcomm QNN)
│   ├── SecurityEvent Schema (Standard 12-feature telemetry schema)
│   ├── Edge Threat Classifier (Local ONNX Runtime / QNN NPU inference)
│   ├── Grounded Explainer Engine (Non-hallucinating evidence generator)
│   └── Triage & Prioritization Engine (P1 Critical / P2 Anomalous / P3 Normal)
│
├── 🐉 Snapdragon Hardware Acceleration (Qualcomm QNN Abstraction)
│   ├── Primary: QNNExecutionProvider (Snapdragon Hexagon NPU)
│   ├── Fallback 1: DmlExecutionProvider (DirectML GPU)
│   └── Fallback 2: CPUExecutionProvider (OpenMP CPU Development Fallback)
│
└── 🎨 Neo-Brutalism Flask Dashboard
    ├── ⚡ Q-Sentinel Edge Dashboard (Live AI + Deterministic split callout)
    └── 🛡️ Legacy Laboratories (QDS Lab, Shor, Grover, PQC, Risk Engine)
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
*(All 53 unit tests passing: 43 baseline QDS tests + 10 edge AI / Snapdragon runtime tests).*

### 3. Train Model & Export ONNX Classifier
```bash
python src/qds_detector/edge_ai/train.py
```

### 4. Launch Q-Sentinel Edge Dashboard
```bash
python wsgi.py
```
Open **`http://localhost:5000/edge`** in your browser.

---

## 📂 Repository Structure

```
.
├── wsgi.py                      # Flask server WSGI entrypoint script
├── requirements.txt              # Dependency specification (Qiskit, Flask, ONNX Runtime, Pytest)
├── flask_app/                   # Flask Web Application & Neo-Brutalism UI
│   ├── routes.py                # Page routes & REST APIs (/api/edge/analyze, /api/edge/status, etc.)
│   └── templates/
│       ├── base.html            # Base template & navigation
│       ├── edge_dashboard.html  # ⚡ Q-Sentinel Edge Snapdragon AI Dashboard
│       └── qds_lab.html         # 🛡️ QDS Teleportation Threat Lab
├── src/
│   └── qds_detector/
│       ├── config.py            # Dataclasses (ExperimentConfig, SessionContext, ThresholdConfig)
│       ├── protocol.py          # End-to-end QDS protocol orchestrator
│       ├── detector.py          # Deterministic 3-state decision engine (ACCEPT/SUSPICIOUS/REJECT)
│       ├── edge_ai/             # [NEW] On-Device Edge AI Intelligence Layer
│       │   ├── schema.py        # SecurityEvent typed dataclass & JSON schema
│       │   ├── features.py      # 12-feature telemetry extractor
│       │   ├── classifier.py    # Local ONNX / QNN threat classifier
│       │   ├── explainer.py     # Grounded non-hallucinating evidence generator
│       │   ├── triage.py        # Priority triage engine (P1 / P2 / P3)
│       │   ├── dataset_generator.py # Simulation-backed synthetic dataset generator
│       │   └── train.py         # Model training & ONNX export script
│       ├── snapdragon/          # [NEW] Qualcomm Snapdragon & QNN Abstraction
│       │   ├── runtime.py       # ONNX Runtime provider hierarchy manager
│       │   ├── qnn_backend.py   # Qualcomm QNN Execution Provider detector
│       │   ├── model_info.py   # Hardware & metadata reporter
│       │   └── benchmark.py     # Empirical latency & throughput benchmarker
│       └── models/              # [NEW] Exported ONNX Model Artifacts
│           └── q_sentinel_threat_classifier.onnx
├── tests/                       # Automated unit test suite (53 passing tests)
└── docs/                        # Technical architecture & deployment documentation
    └── snapdragon_qnn_deployment.md # Snapdragon HP PC deployment guide
```

---

## 🔒 Privacy & Snapdragon NPU Hardware Transparency

- **100% Local On-Device Processing**: Telemetry is analyzed locally on the Snapdragon host—zero cloud network calls.
- **Truthful Hardware Reporting**: The UI queries `onnxruntime.get_available_providers()` and displays `QNNExecutionProvider (Hexagon NPU)` on Snapdragon hardware or `CPUExecutionProvider` on Ubuntu development machines without fabricating metrics.

---

## 📜 References & Standards
1. Snapdragon® AI Lab Build & Present Challenge, Qualcomm, 2026.
2. Smart India Hackathon 2026, Problem Statement SIH26141, Egreen Quanta.
3. Qualcomm Neural Processing SDK / QNN Execution Provider Documentation.
