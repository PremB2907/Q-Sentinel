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

### Visual Matrix Diagram
```
             Measurement Basis
             Z        X        Y
          ┌────────┬────────┬────────┐
X Error   │   🔴   │   🟢   │   🔴   │
          ├────────┼────────┼────────┤
Z Error   │   🟢   │   🔴   │   🔴   │
          └────────┴────────┴────────┘

🟢 Commuting / Invariant (PASS)
🔴 Non-commuting / Observable (REJECT)

"The detector reproduces the expected algebraic observability pattern."
```

### Empirical Per-Basis Matrix ($\lambda = 0.35, N = 5000$)
| Attack Vector | Z-Basis | X-Basis | Y-Basis | Aggregate Detection | Commuting Algebra Rationale |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **State Forgery** | **100% (REJECT)** | **100% (REJECT)** | **100% (REJECT)** | **100.0%** | Non-orthogonal state perturbation shifts all projection distributions. |
| **Depolarizing Noise** | **100% (REJECT)** | **100% (REJECT)** | **100% (REJECT)** | **100.0%** | Isotropic depolarizing noise affects all measurement operators. |
| **Bit-Flip Noise ($X$)** | **100% (REJECT)** | **0% (PASS)** | **100% (REJECT)** | **66.7%** | $X|+\rangle = |+\rangle$. In $X$-basis, bit-flip leaves eigenstate invariant. |
| **Phase-Flip Noise ($Z$)** | **0% (PASS)** | **100% (REJECT)** | **100% (REJECT)** | **66.7%** | $Z|0\rangle = |0\rangle$. In $Z$-basis, phase-flip leaves eigenstate invariant. |

### 🎙️ Presenter Verbal Script (20 Seconds)
> *"The interesting result is not simply that attacks are detected. It is that the detector reproduces the expected Pauli observability pattern. An X error is invisible in the X eigenbasis, while Z and Y measurements expose it. Similarly, a Z error is invisible in the Z eigenbasis. This experimentally validates the basis-dependent behavior predicted by the underlying operator algebra."*

---

## Slide 10: Conclusion, 2-3 Minute Pitch & 15 Judge Q&A Cheatsheet

### 🎤 2–3 Minute Pitch Script
> *"Good morning respected judges. We present **Q-Sentinel**, a quantum-statistical threat detection system built for Smart India Hackathon problem statement SIH26141 under Egreen Quanta.*  
>
> *Classical digital signatures face imminent vulnerability from quantum algorithms. While Quantum Digital Signatures (QDS) provide state-transfer security, detecting real-time threat vectors without black-box machine learning models is a key challenge.*  
>
> *Our solution implements a **Two-Tier Rule-Based Architecture** driven strictly by quantum statistical hypothesis testing with **zero AI/ML**. Tier 1 traps protocol-layer replay and impersonation attacks using session context nonces and identity keys, achieving **100% detection**. Tier 2 traps physical state forgery and channel noise using projective measurement outcome distributions, $z$-score hypothesis tests, and state fidelity.*  
>
> *In our 1,410-experiment benchmark, Q-Sentinel achieved **0.0% False Reject Rate** on legitimate traffic. Most importantly, our experiment validates the underlying Pauli operator algebra: single-basis $X$ errors leave $X$-basis eigenstates invariant, while non-commuting $Z$ and $Y$ bases detect the perturbation—yielding an exact 66.7% single-basis aggregate observability pattern.*  
>
> *Q-Sentinel is not presented as an unconditional security proof, but as an experimentally validated, rule-based threat detector. Thank you!"*

### 🧠 15 Aggressive Judge Questions & Answers Cheatsheet

1. **Q: Why did you not use Machine Learning / AI?**  
   *A: SIH26141 requires a quantum-principle-based detector. ML models introduce black-box decision boundaries and false acceptances. Deterministic quantum statistics ($z$-scores, $\chi^2$, fidelity) provide verifiable confidence.*

2. **Q: Why didn't you detect 100% of bit-flip attacks in aggregate?**  
   *A: Because detecting $X$ errors in an $X$ basis would contradict Pauli algebra. $X |+\rangle = |+\rangle$, so $X$ errors are invariant in $X$-basis. Non-commuting $Z$ and $Y$ bases achieve 100% detection, giving 66.7% single-basis aggregate observability.*

3. **Q: Is this prototype quantum-secure?**  
   *A: Q-Sentinel is not presented as a proof of unconditional quantum security. It detects the modeled attack classes within the evaluated threat model.*

4. **Q: So what exactly have you proven?**  
   *A: We have experimentally validated our detection model under defined simulation conditions. The protocol layer detects evaluated replay/impersonation, while the quantum layer reproduces Pauli basis-dependent observability.*

5. **Q: How did you derive your 0.0100 acceptance threshold?**  
   *A: Derived empirically via clean calibration trials. Under noise-aware sampling ($p_{\text{noise}}=0.005$), the 99th percentile deviation is $\approx 0.0058$. We apply an operational safety margin ($0.0100$) to absorb environmental drift.*

6. **Q: Can quantum measurements detect a replayed signature?**  
   *A: No. Replayed transcripts have physically valid quantum statistics. Replay must be detected at Tier 1 using nonces and timestamps.*

7. **Q: What is the difference between FPR and FAR in your report?**  
   *A: FPR/FRR measures false rejects on clean legitimate traffic (0.0% in our baseline). FAR measures false accepts on attack traffic.*

8. **Q: What quantum SDK and simulator are you running?**  
   *A: Qiskit 2.x and Qiskit Aer backend with explicit unitary state preparation gates ($H, S, X$).*

9. **Q: How many total experiments did you run for evaluation?**  
   *A: 1,410 independent trials (30 clean + 1,380 attack instances across severities $\lambda \in [0, 1]$).*

10. **Q: Are calibration and evaluation datasets separate?**  
    *A: Yes, completely non-overlapping datasets with distinct random seed offsets.*

11. **Q: How fast is the detector?**  
    *A: End-to-end simulation and analysis takes under 2.5 ms per 5,000-shot experiment.*

12. **Q: Does this run offline?**  
    *A: Yes, 100% offline execution with local Qiskit Aer simulation.*

13. **Q: What happens if shot count N is reduced to 1,000?**  
    *A: Binomial standard error increases from $0.007$ to $0.015$. Thresholds scale dynamically via $SE = \sqrt{p_0(1-p_0)/N}$.*

14. **Q: How do you handle density matrices in channel noise attacks?**  
    *A: Density matrices $\rho$ evaluate trace probabilities $p_\pm = \mathrm{Tr}(P_\pm \rho)$ under projective measurement operators.*

15. **Q: What is the current release tag?**  
    *A: `v0.4.0-experimental`, frozen and fully reproducible on GitHub.*

### 🔑 Three Core Axioms
1. **100% detection $\neq$ 100% security**
2. **0% FRR $\neq$ zero false positives in every possible environment**
3. **66.7% observability $\neq$ detector failure**

