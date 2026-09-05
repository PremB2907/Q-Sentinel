# Quantum Attack & Cryptanalysis Threat Model

SIH26141 • Egreen Quanta

This document details the theoretical foundations, attack models, resource estimation formulas, and scientific limitations of the **Classical Signature Quantum Threat Analysis** domain in Q-Sentinel.

---

## 1. Overview & Defensive Scope

While the primary **Q-Sentinel** detector addresses **Quantum Digital Signatures (QDS)** using continuous teleportation state verification, legacy infrastructure relies on classical public-key infrastructure (PKI) such as RSA, ECDSA, and Ed25519.

To provide a complete security laboratory, Q-Sentinel includes a classical threat analysis module that models:
1. **Shor's Integer Factorization** targeting RSA.
2. **Shor's Discrete Logarithm Attack** targeting Elliptic Curve Cryptography (ECDSA/Ed25519).
3. **Grover's Quadratic Preimage Search** targeting hash-based and symmetric key constructions.
4. **Fault-Tolerant Surface Code Resource Estimation** for physical quantum hardware.
5. **Post-Quantum Cryptography (PQC)** standards (NIST FIPS 204 ML-DSA and FIPS 205 SLH-DSA).

---

## 2. Scientific Limitations & Guardrails

> [!IMPORTANT]
> **Defensible Research Framing**:
> - Interactive demonstrations for Shor and ECC discrete log run on **educational toy-scale parameters** ($N \in \{15, 21, 35, 77\}$ or small prime fields $\mathbb{F}_p$).
> - Real-world parameter evaluation (e.g. RSA-2048 or ECDSA P-256) is handled exclusively by a dedicated **resource estimation model** based on fault-tolerant surface code literature.
> - Q-Sentinel **NEVER** claims to have practically broken production-scale RSA or ECDSA in a classical software simulation.

---

## 3. Mathematical Foundations

### 3.1 Shor's Algorithm (Polynomial Time $O(n^3)$)
Shor's algorithm reduces integer factorization $N = p \cdot q$ to period finding of the function:
$$f(x) = a^x \pmod N$$

1. Choose coprime base $a < N$.
2. Construct quantum state using Quantum Phase Estimation (QPE) to extract period $r$.
3. If $r$ is even and $a^{r/2} \not\equiv -1 \pmod N$, extract non-trivial factors via:
   $$p, q = \gcd(a^{r/2} \pm 1, N)$$

### 3.2 Elliptic Curve Discrete Logarithm (ECDLP)
For a public key $Q = k \cdot G$ over $E(\mathbb{F}_p)$, Shor's 2D QPE state constructs:
$$|\psi\rangle = \frac{1}{n} \sum_{x, y=0}^{n-1} |x\rangle |y\rangle |xG + yQ\rangle$$
Measuring the periodicity reveals scalar $k$ in polynomial time $O(n^3)$.

### 3.3 Grover's Quadratic Search ($O(\sqrt{N})$)
For a search space of size $N = 2^k$, Grover's diffusion operator amplifies target state amplitude in:
$$M = \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor \text{ iterations}$$
Unlike Shor, Grover provides a quadratic speedup $O(\sqrt{N})$, which halves effective symmetric key lengths (e.g., AES-128 $\rightarrow$ 64 bits of security), but does NOT instantly break asymmetric signature structures.

---

## 4. CRQC Resource Estimation Methodology

Logical qubit and physical surface code qubit requirements are derived from Beauregard (2002), Roetteler et al. (2017), and Gidney & Ekerå (2021):

| Target Algorithm | Logical Qubits ($Q_L$) | T-Gate Count ($T_c$) | Estimated Physical Qubits ($P_{err} = 10^{-3}$) |
| :--- | :--- | :--- | :--- |
| **RSA-1024** | $2n + 2 \approx 2,050$ | $\sim 3.4 \times 10^{10}$ | $\sim 1.2 \times 10^6$ |
| **RSA-2048** | $2n + 2 \approx 4,098$ | $\sim 2.7 \times 10^{11}$ | $\sim 2.5 \times 10^6$ |
| **ECDSA P-256** | $9n + \lceil \log_2 n \rceil \approx 2,312$ | $\sim 8.0 \times 10^{8}$ | $\sim 3.8 \times 10^5$ |
| **ECDSA P-384** | $9n + \lceil \log_2 n \rceil \approx 3,465$ | $\sim 2.7 \times 10^{9}$ | $\sim 6.2 \times 10^5$ |

---

## 5. Mosca Theorem & Risk Engine

Risk classification is determined deterministically via Mosca's Theorem:
$$\text{If } X + Y > Z \implies \text{CRITICAL RISK}$$
Where:
- $X$: Data retention requirement (years signature/data must remain secure).
- $Y$: Migration time to transition infrastructure to PQC / QDS (years).
- $Z$: Estimated timeline to a Cryptographically Relevant Quantum Computer (~15 years baseline).
