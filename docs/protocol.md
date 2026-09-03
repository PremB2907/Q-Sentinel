# Q-Sentinel: Quantum Digital Signature (QDS) Threat Detection Architecture

**Problem Statement**: SIH26141 — Quantum-Inspired Cyber Threat Detection for Digital Signature Security  
**Sponsor**: Egreen Quanta  
**Core Directive**: Deterministic, rule-based threat detection for QDS protocols using quantum measurement statistics and projective measurements. **STRICTLY NO AI/ML**.

---

## 1. System Architecture

```
User / Demo Operator (Streamlit UI)
         │
         ▼
Experiment Orchestrator (protocol.py)
 ├── QDS Simulator (Qiskit + Aer)
 │    ├── 6 Pauli Eigenstates (|0>, |1>, |+>, |->, |+i>, |-i>)
 │    ├── Entangled Bell State |Phi+> = (|00> + |11>) / sqrt(2)
 │    └── 3-Qubit Quantum Teleportation + Conditional Pauli Corrections
 │
 ├── Threat Engine (attacks.py)
 │    ├── State Forgery (State Perturbation Mixture: (1-λ)ρ_legit + λ ρ_forge)
 │    ├── Quantum Channel Noise (Bit-Flip, Phase-Flip, Depolarizing)
 │    ├── Replay Attack (Stale Nonce / Session Reuse)
 │    └── Impersonation Attack (Signer Identity Context Mismatch)
 │
 └── Deterministic Detector (detector.py)
      ├── Projective Measurements P± = (I ± σ) / 2
      ├── Binomial Confidence Bounds & Standard Error
      ├── z-Score & Chi-Square Goodness-of-Fit Tests
      └── Rule Evaluation: ACCEPT / SUSPICIOUS / REJECT
```

---

## 2. Mathematical Foundation

### 2.1 Pauli Basis Eigenstates
| Basis | Observable | +1 Eigenstate | -1 Eigenstate | Projectors |
| :--- | :---: | :---: | :---: | :--- |
| **Computational** | $Z$ | $|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ | $|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$ | $P_\pm^Z = \frac{I \pm Z}{2}$ |
| **Hadamard** | $X$ | $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ | $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$ | $P_\pm^X = \frac{I \pm X}{2}$ |
| **Phase** | $Y$ | $|+i\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}}$ | $|-i\rangle = \frac{|0\rangle - i|1\rangle}{\sqrt{2}}$ | $P_\pm^Y = \frac{I \pm Y}{2}$ |

### 2.2 Quantum Teleportation & Corrections
Teleportation transfers an input qubit state $|\psi\rangle$ using an entangled Bell pair $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$.
Bell measurement on sender qubits yields classical bits $(b_A, b_B)$:

| Bell Outcome $(b_A, b_B)$ | Receiver Correction | Transformation |
| :---: | :---: | :--- |
| $00$ | $I$ | No operation |
| $01$ | $X$ | Bit flip |
| $10$ | $Z$ | Phase flip |
| $11$ | $ZX$ | Bit and phase flip |

---

## 3. Threat Detection Rules (Deterministic & Rule-Based)

```
                       [ Incoming QDS Verification Request ]
                                         │
                         ┌───────────────┴───────────────┐
                         │ Identity Context Match?       │
                         └───────────────┬───────────────┘
                                   No    │    Yes
                               ┌─────────┴─────────┐
                               ▼                   ▼
                           [ REJECT ]     [ Freshness Nonce Valid? ]
                        (Impersonation)            │
                                           No      │    Yes
                                       ┌───────────┴───────────┐
                                       ▼                       ▼
                                   [ REJECT ]         [ Compute Statistics ]
                                   (Replay)           - Fidelity F
                                                      - Max Deviation
                                                      - z-Score / p-value
                                                               │
                                         ┌─────────────────────┴─────────────────────┐
                                         │ Pass Calibrated Acceptance Thresholds?    │
                                         └─────────────────────┬─────────────────────┘
                                                   Yes         │         No
                                           ┌───────────────────┼───────────────────┐
                                           ▼                   ▼                   ▼
                                      [ ACCEPT ]         [ SUSPICIOUS ]       [ REJECT ]
                                     (Legitimate)       (Near Threshold)     (High Shift)
```

---

## 4. Verification & Testing

Run full unit test suite:
```bash
pytest tests/ -v
```

Launch interactive Streamlit dashboard:
```bash
streamlit run app.py
```
