# SIH26141 Presentation Deck Specification

**Project Title**: Q-Sentinel: Quantum-Statistical Threat Detection for Teleportation-Based Digital Signatures  
**Problem Statement ID**: SIH26141  
**Category**: Software / Blockchain & Cybersecurity  
**Sponsor**: Egreen Quanta  
**Version**: `v0.4.0-experimental`

---

## Slide 1: Title Slide & Problem Summary

### Title
**Q-Sentinel**  
*Quantum-Statistical Threat Detection for Teleportation-Based Digital Signatures*

### Subtitle
Problem Statement SIH26141 • Egreen Quanta • Blockchain & Cybersecurity

### Core Principle Callout
> **Rule-Based Quantum Statistical Hypothesis Testing • Zero AI/ML Models**

---

## Slide 2: Problem Statement & Motivation

### Cyber Security Challenge
- Classical digital signatures (RSA/ECDSA) face vulnerabilities from quantum algorithms (Shor's Algorithm).
- Quantum Digital Signatures (QDS) provide quantum-secure signing primitives via entanglement and quantum states.
- **Problem**: Detecting signature forgery, impersonation, replay attacks, and quantum channel manipulation **without relying on uninterpretable ML models**.

### SIH Directive
- SIH26141 explicitly requires a quantum-principle-based threat detector using Pauli eigenstates, projective measurements, and statistical decision rules.

---

## Slide 3: System Architecture (Two-Tier Threat Model)

```
                    Q-SENTINEL ARCHITECTURE
                               │
              ┌────────────────┴────────────────┐
              │                                 │
       TIER 1: PROTOCOL LAYER           TIER 2: QUANTUM LAYER
       - Identity Key Context           - 6 Pauli Basis Eigenstates
       - Nonce & Session Freshness      - Projective Measurements P±
              │                                 │
       ┌──────┴──────┐                  ┌───────┴────────┐
       │             │                  │                │
 Impersonation    Replay             Forgery       Channel Noise
   Detection     Detection          Detection        Detection
 (100% Rate)    (100% Rate)       (100% λ≥0.05)     (Basis-Matrix)
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                   DETERMINISTIC DECISION
               [ ACCEPT / SUSPICIOUS / REJECT ]
```

---

## Slide 4: Quantum Core Physics & Teleportation Primitive

### 1. Pauli Basis Eigenstates
- **Z-basis (Computational)**: $|0\rangle, |1\rangle$
- **X-basis (Hadamard)**: $|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}, |-\rangle = \frac{|0\rangle-|1\rangle}{\sqrt{2}}$
- **Y-basis (Phase)**: $|+i\rangle = \frac{|0\rangle+i|1\rangle}{\sqrt{2}}, |-i\rangle = \frac{|0\rangle-i|1\rangle}{\sqrt{2}}$

### 2. Teleportation Protocol
- Entangled Bell Pair preparation: $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$
- 3-qubit teleportation circuit with explicit unitary gates ($H, S, X$) and classical Bell measurement outcome bits $(b_A, b_B)$.
- Conditional Pauli corrections: $I, X, Z, ZX$.

---

## Slide 5: Statistical Threat Detector (No AI/ML)

### Decision Rationale
> *"The problem specification requires a quantum-principle-based detector without AI/ML. Our approach therefore uses directly interpretable measurement statistics, calibrated confidence bounds, and deterministic hypothesis-testing rules. Every decision can be traced back to an observable quantum measurement rather than a learned model."*

### Mathematical Framework
- **Projective Measurements**: $P_\pm = \frac{I \pm \sigma}{2}, \quad p_\pm = \mathrm{Tr}(P_\pm \rho)$
- **Hypothesis Testing**: $\hat{p} = \frac{k}{N}, \quad SE = \sqrt{\frac{p_0(1-p_0)}{N}}, \quad z = \frac{\hat{p}-p_0}{SE}$
- **Goodness-of-Fit**: Chi-Square statistic $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ with 2-sided $p$-value.

---

## Slide 6: Empirical Threshold Calibration

### Methodology
- Evaluated $M=100$ independent clean calibration trials across $Z, X, Y$ bases under ideal and noise-aware ($p_{\text{noise}} = 0.005$) simulator profiles.
- Derived empirical 99th percentile ($\alpha=0.01$) acceptance threshold bounds per basis.

### Empirical Calibration Summary
| Basis | Mean Deviation ($\bar{\Delta}$) | 99th Percentile Deviation ($\Delta_{99}$) | Operational Acceptance Threshold ($\Delta_{\text{thresh}}$) |
| :---: | :---: | :---: | :---: |
| **Z** | $0.0032$ | $0.0056$ | **$0.0100$** |
| **X** | $0.0032$ | $0.0050$ | **$0.0100$** |
| **Y** | $0.0034$ | $0.0058$ | **$0.0100$** |

> *Defense Note*: The empirical 99th percentile establishes the clean-operation boundary under channel noise ($\approx 0.0058$); an operational safety margin of $0.0100$ is applied to accommodate environmental drift.

---

## Slide 7: Per-Basis Attack Observability Matrix (The Physics Slide 🌶️)

### Empirical Per-Basis Matrix ($\lambda = 0.35, N = 5000$)
| Attack Vector | Z-Basis | X-Basis | Y-Basis | Aggregate Detection | Commuting Algebra Rationale |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **State Forgery** | **100% (REJECT)** | **100% (REJECT)** | **100% (REJECT)** | **100.0%** | Non-orthogonal state perturbation shifts all projection distributions. |
| **Depolarizing Noise** | **100% (REJECT)** | **100% (REJECT)** | **100% (REJECT)** | **100.0%** | Isotropic depolarizing noise affects all measurement operators. |
| **Bit-Flip Noise ($X$)** | **100% (REJECT)** | **0% (PASS)** | **100% (REJECT)** | **66.7%** | $X|+\rangle = |+\rangle$. In $X$-basis, bit-flip leaves eigenstate invariant. |
| **Phase-Flip Noise ($Z$)** | **0% (PASS)** | **100% (REJECT)** | **100% (REJECT)** | **66.7%** | $Z|0\rangle = |0\rangle$. In $Z$-basis, phase-flip leaves eigenstate invariant. |

### Physics Finding Statement
> *"Demonstrating, under the evaluated threat model, that Pauli errors commuting with the measured observable can remain undetectable in that basis, while complementary non-commuting measurements expose the disturbance."*

---

## Slide 8: Experimental Security Benchmark Results

### Summary Table (1,410 Independent Trials)
| Scenario Category | Attack Type | Detection Rate (TPR) | False Accept Rate (FAR) | False Reject Rate (FRR) |
| :--- | :--- | :---: | :---: | :---: |
| **Legitimate Traffic** | **Clean Baseline** | — | — | **0.0%** |
| **Protocol Layer** | **Replay** | **100.0%** | **0.0%** | **0.0%** |
| **Protocol Layer** | **Impersonation** | **100.0%** | **0.0%** | **0.0%** |
| **Quantum Layer** | **State Forgery** | **90.9%** (100% for $\lambda \ge 0.05$) | **9.1%** (0.0% for $\lambda \ge 0.05$) | **0.0%** |
| **Quantum Layer** | **Depolarizing Noise** | **90.9%** (100% for $\lambda \ge 0.05$) | **9.1%** (0.0% for $\lambda \ge 0.05$) | **0.0%** |
| **Quantum Layer** | **Bit-Flip Noise** | **60.6%** (66.7% per-basis) | **39.4%** | **0.0%** |
| **Quantum Layer** | **Phase-Flip Noise** | **60.6%** (66.7% per-basis) | **39.4%** | **0.0%** |

### Verified Security Summary
> *"Q-Sentinel achieved zero false rejects on legitimate traffic (FPR = 0%, FRR = 0%) and 100% protocol-layer detection for the evaluated replay and impersonation scenarios. In quantum-layer experiments, Q-Sentinel detects the modeled attack classes within the evaluated threat model, achieving 100% detection for state forgery and depolarizing attacks at severities $\lambda \ge 0.05$."*

---

## Slide 9: Hero UI Demo Flow & Operational Features

1. **Clean Teleportation Validation**: Select $|+i\rangle$, Basis $Y$, Shots $5000$ $\to$ Click Run $\to$ 🟢 **SIGNATURE VALIDATED** (Fidelity $1.0000$, $\Delta = 0.0000$).
2. **State Forgery Injection**: Select State Forgery, Severity $\lambda = 0.35$ $\to$ Click Run $\to$ 🔴 **SIGNATURE REJECTED** (Threat: `STATISTICAL SIGNATURE FORGERY`, Fidelity $0.8250$, $\Delta = 0.1750$, $p$-value $< 0.001$).
3. **Replay Attack Demonstration**: Select Replay Attack $\to$ Click Run $\to$ 🔴 **SIGNATURE REJECTED** (Tier 1 Freshness Failure: `STALE REPLAY TRANSCRIPT`).
4. **Impersonation Demonstration**: Select Impersonation Attack $\to$ Click Run $\to$ 🔴 **SIGNATURE REJECTED** (Tier 1 Identity Failure: `SIGNER IMPERSONATION`).

---

## Slide 10: Conclusion & Engineering Roadmap

### Key Takeaways
1. **SIH26141 Compliant**: Fully rule-based quantum statistical threat detector without AI/ML algorithms.
2. **Two-Tier Architecture**: Clean separation between protocol context verification and quantum measurement statistics.
3. **Scientifically Defensible**: Derived empirical basis thresholds and validated commuting Pauli matrix behavior.

### Repository & Code Standard
- **GitHub Repository**: [https://github.com/PremB2907/Q-Sentinel](https://github.com/PremB2907/Q-Sentinel)
- **Experimental Tag**: `v0.4.0-experimental`
- **Test Suite**: 25/25 Pytest unit tests passing cleanly.
