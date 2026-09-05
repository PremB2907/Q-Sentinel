"""
Q-Sentinel: Quantum Cyber Threat Laboratory for Digital Signature Security.
SIH26141 • Egreen Quanta
Streamlit Interactive Security Laboratory UI.
"""

import time
import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Domain A: QDS Baseline
from qds_detector.config import ExperimentConfig, SessionContext, ThresholdConfig
from qds_detector.states import PAULI_STATES, STATE_ALIASES, get_expected_probabilities
from qds_detector.protocol import run_qds_experiment

# Domain B & C: Classical Threats, PQC & Risk Engine
from qds_detector.quantum_attacks.shor import run_shor_factorization
from qds_detector.quantum_attacks.ecc_analysis import analyze_ecc_dlog_threat
from qds_detector.quantum_attacks.grover import run_grover_search_analysis
from qds_detector.quantum_attacks.resource_estimator import estimate_crqc_resources
from qds_detector.quantum_attacks.pqc_analysis import get_pqc_scheme_metadata, list_pqc_schemes
from qds_detector.quantum_attacks.quantum_risk import evaluate_quantum_risk


# Page Configuration
st.set_page_config(
    page_title="Q-Sentinel | Quantum Cyber Threat Laboratory",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .hero-accept {
        background: linear-gradient(135deg, rgba(46, 160, 67, 0.25) 0%, rgba(46, 160, 67, 0.05) 100%);
        border: 2px solid #2ea043;
        box-shadow: 0 0 20px rgba(46, 160, 67, 0.3);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero-reject {
        background: linear-gradient(135deg, rgba(248, 81, 73, 0.25) 0%, rgba(248, 81, 73, 0.05) 100%);
        border: 2px solid #f85149;
        box-shadow: 0 0 20px rgba(248, 81, 73, 0.3);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero-suspicious {
        background: linear-gradient(135deg, rgba(210, 153, 34, 0.25) 0%, rgba(210, 153, 34, 0.05) 100%);
        border: 2px solid #d29922;
        box-shadow: 0 0 20px rgba(210, 153, 34, 0.3);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero-title-accept { color: #3fb950; font-size: 32px; font-weight: 900; letter-spacing: 2px; }
    .hero-title-reject { color: #f85149; font-size: 32px; font-weight: 900; letter-spacing: 2px; }
    .hero-title-suspicious { color: #e3b341; font-size: 32px; font-weight: 900; letter-spacing: 2px; }
    .hero-threat-tag {
        background-color: rgba(248, 81, 73, 0.2);
        color: #ff7b72;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        margin-top: 8px;
    }
    .tier-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .badge-no-ai {
        background-color: #1f6feb;
        color: #ffffff;
        font-size: 11px;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .notice-box {
        background-color: rgba(56, 139, 253, 0.1);
        border-left: 4px solid #58a6ff;
        padding: 12px;
        margin-bottom: 16px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.image("https://img.shields.io/badge/Q--Sentinel-v0.5.0--research-blue", use_container_width=True)
st.sidebar.title("🛡️ Q-Sentinel Labs")
st.sidebar.caption("Quantum Cyber Threat Laboratory for Digital Signatures")

lab_choice = st.sidebar.radio(
    "Select Security Domain / Laboratory:",
    [
        "🛡️ QDS Threat Lab (SIH26141 Baseline)",
        "⚡ Classical Signature Threats Overview",
        "🔢 Shor Factorization Laboratory",
        "🔍 Grover Key Search Laboratory",
        "📜 Post-Quantum (PQC) Comparison",
        "📊 Unified Quantum Risk Assessment"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<span class='badge-no-ai'>STRICT RULE ENGINE • NO AI/ML</span>", unsafe_allow_html=True)
st.sidebar.caption("SIH Problem Statement: SIH26141")


# ==============================================================================
# TAB 1: QDS THREAT LAB (SIH26141 BASELINE UNTOUCHED)
# ==============================================================================
if lab_choice == "🛡️ QDS Threat Lab (SIH26141 Baseline)":
    st.markdown("### 🛡️ Quantum Digital Signature (QDS) Teleportation Security Laboratory")
    st.markdown("""
    <div class='notice-box'>
    <b>SIH26141 Primary Module:</b> Continuous physical verification of 3-qubit teleported Bell states 
    (\\(|\\Phi^+\\rangle = \\frac{|00\\rangle + |11\\rangle}{\\sqrt{2}}\\)) across 6 Pauli eigenstates using deterministic statistical thresholds (z-score, Chi-Square).
    </div>
    """, unsafe_allow_html=True)

    col_setup, col_params = st.columns([1, 2])

    with col_setup:
        st.subheader("⚙️ Experiment Controls")
        
        state_label = st.selectbox(
            "Pauli Eigenstate (|ψ⟩):",
            list(PAULI_STATES.keys()),
            index=0
        )
        
        basis_choice = st.selectbox(
            "Projective Measurement Basis:",
            ["X", "Y", "Z"],
            index=2
        )
        
        shots = st.slider("Quantum Measurement Shots:", 100, 5000, 1000, step=100)
        
        st.markdown("---")
        st.subheader("🔥 Threat Injection Vector")
        attack_type = st.radio(
            "Select Attack Model:",
            ["Clean (Legitimate)", "State Forgery", "Bit-Flip Noise", "Phase-Flip Noise", "Depolarizing Noise", "Replay Attack", "Impersonation Attack"]
        )
        
        severity_lambda = 0.0
        if attack_type in ["State Forgery", "Bit-Flip Noise", "Phase-Flip Noise", "Depolarizing Noise"]:
            severity_lambda = st.slider("Attack Severity (λ):", 0.0, 1.0, 0.35, step=0.05)

    with col_params:
        # Construct experiment context & config
        exp_attack_type = "clean"
        if attack_type == "State Forgery": exp_attack_type = "state_forgery"
        elif attack_type == "Bit-Flip Noise": exp_attack_type = "bit_flip"
        elif attack_type == "Phase-Flip Noise": exp_attack_type = "phase_flip"
        elif attack_type == "Depolarizing Noise": exp_attack_type = "depolarizing"
        elif attack_type == "Replay Attack": exp_attack_type = "replay"
        elif attack_type == "Impersonation Attack": exp_attack_type = "impersonation"

        ctx = SessionContext(
            nonce="valid_nonce_1001" if attack_type != "Replay Attack" else "expired_nonce_999",
            signer_id="Alice_PubKey_0x8F4A" if attack_type != "Impersonation Attack" else "Eve_Mallory",
            expected_signer_id="Alice_PubKey_0x8F4A"
        )
        
        config = ExperimentConfig(
            input_state=state_label,
            measurement_basis=basis_choice,
            shots=shots,
            attack_type=exp_attack_type,
            attack_severity=severity_lambda,
            session_context=ctx
        )

        res = run_qds_experiment(config)
        
        status = res.get("decision", "ACCEPT")
        z_score = res.get("z_score", 0.0)
        p_val = res.get("p_value", 1.0)
        fidelity = res.get("fidelity", 1.0)
        reason = res.get("reason", "")
        reasons = [r.strip() for r in reason.split(";") if r.strip()] if reason else []

        # Hero Callout Card
        if status == "ACCEPT":
            st.markdown(f"""
            <div class='hero-accept'>
                <div class='hero-title-accept'>✅ DECISION: ACCEPT</div>
                <div><b>Legitimate Teleportation Signature Verified</b></div>
                <div style='margin-top: 8px;'>z-score: {z_score:.2f} | Chi2 p-val: {p_val:.4f} | Fidelity: {fidelity:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        elif status == "REJECT":
            reasons_html = "".join([f"<div class='hero-threat-tag'>🚨 {r}</div><br/>" for r in reasons]) if reasons else "<div class='hero-threat-tag'>🚨 Quantum Verification Failed</div>"
            st.markdown(f"""
            <div class='hero-reject'>
                <div class='hero-title-reject'>❌ DECISION: REJECT</div>
                <div><b>Quantum Security Threshold Breach Detected!</b></div>
                <div style='margin-top: 8px;'>{reasons_html}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            reasons_html = "".join([f"<div class='hero-threat-tag'>⚠️ {r}</div><br/>" for r in reasons]) if reasons else "<div class='hero-threat-tag'>⚠️ Statistical Anomaly</div>"
            st.markdown(f"""
            <div class='hero-suspicious'>
                <div class='hero-title-suspicious'>⚠️ DECISION: SUSPICIOUS</div>
                <div><b>Anomalous Measurement Distribution Detected</b></div>
                <div style='margin-top: 8px;'>{reasons_html}</div>
            </div>
            """, unsafe_allow_html=True)

        # Plotly Distribution Chart
        obs_probs = res.get("observed_probability", {"0": 0.5, "1": 0.5})
        base_probs = res.get("baseline_probability", {"0": 0.5, "1": 0.5})
        
        df_chart = pd.DataFrame({
            "Outcome": ["|0⟩ (+1)", "|1⟩ (-1)"],
            "Measured Probability": [obs_probs.get("0", 0.0), obs_probs.get("1", 0.0)],
            "Expected Clean Probability": [base_probs.get("0", 0.5), base_probs.get("1", 0.5)]
        })
        
        fig = px.bar(
            df_chart, 
            x="Outcome", 
            y=["Measured Probability", "Expected Clean Probability"],
            barmode="group",
            title=f"Teleportation Measurement Distribution in {basis_choice}-basis (Shots={shots})",
            color_discrete_sequence=["#58a6ff", "#2ea043"]
        )
        fig.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", font_color="#c9d1d9")
        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# TAB 2: CLASSICAL SIGNATURE THREATS OVERVIEW
# ==============================================================================
elif lab_choice == "⚡ Classical Signature Threats Overview":
    st.markdown("### ⚡ Classical Digital Signature Quantum-Threat Analysis")
    st.markdown("""
    <div class='notice-box'>
    <b>Research Objective:</b> Evaluate how future Cryptographically Relevant Quantum Computers (CRQCs) threaten 
    legacy digital signature algorithms (RSA, ECDSA, Ed25519) via Shor's and Grover's quantum algorithms.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("RSA-2048 Shor Risk", "CRITICAL", "Shor's Algorithm (Polynomial)")
    c2.metric("ECDSA P-256 Shor Risk", "CRITICAL", "Discrete Log Attack")
    c3.metric("Grover Preimage Impact", "QUADRATIC", "O(N) -> O(sqrt(N))")

    st.markdown("---")
    st.subheader("🔬 Threat Mechanism Comparison")
    
    df_threats = pd.DataFrame([
        {"Scheme": "RSA-2048", "Math Foundation": "Integer Factorization", "Quantum Attack": "Shor's Algorithm", "Asymptotic Complexity": "Polynomial O(n^3)", "Quantum Vulnerability": "CRITICAL"},
        {"Scheme": "ECDSA P-256", "Math Foundation": "Elliptic Curve Discrete Log", "Quantum Attack": "Shor's Discrete Log", "Asymptotic Complexity": "Polynomial O(n^3)", "Quantum Vulnerability": "CRITICAL"},
        {"Scheme": "Ed25519", "Math Foundation": "Edwards Curve Discrete Log", "Quantum Attack": "Shor's Discrete Log", "Asymptotic Complexity": "Polynomial O(n^3)", "Quantum Vulnerability": "CRITICAL"},
        {"Scheme": "AES-256 / SHA-256", "Math Foundation": "Symmetric / Hash Preimage", "Quantum Attack": "Grover's Search", "Asymptotic Complexity": "Quadratic O(sqrt(N))", "Quantum Vulnerability": "LOW (Key Doubling)"},
        {"Scheme": "ML-DSA-44", "Math Foundation": "Module Learning With Errors", "Quantum Attack": "Lattice Reduction", "Asymptotic Complexity": "Exponential", "Quantum Vulnerability": "RESISTANT"},
    ])
    st.table(df_threats)


# ==============================================================================
# TAB 3: SHOR LABORATORY
# ==============================================================================
elif lab_choice == "🔢 Shor Factorization Laboratory":
    st.markdown("### 🔢 Shor's Algorithm Toy Integer Factorization Simulator")
    st.markdown("""
    <div class='notice-box'>
    <b>Educational Toy Simulation:</b> Demonstrates quantum period-finding 
    \\(f(x) = a^x \\pmod N\\) to recover prime factors of semiprimes. 
    <b>Note:</b> Production RSA-2048 requires a physical fault-tolerant CRQC (~4,098 logical qubits).
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        N = st.selectbox("Select Toy Semiprime Modulus (N):", [15, 21, 35, 77, 91, 143], index=0)
        a_choice = st.text_input("Coprime Base (a) [Optional]:", "")
        base_a = int(a_choice) if a_choice.strip().isdigit() else None
        
        run_btn = st.button("🚀 Execute Shor Simulation", use_container_width=True)

    with col2:
        if run_btn or True:
            res = run_shor_factorization(N=N, base_a=base_a)
            
            st.subheader(f"Results for N = {N}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Recovered Factors", f"{res['factors']}" if res['successful'] else "Failed")
            m2.metric("Discovered Period (r)", f"{res['period_r']}" if res['period_r'] else "N/A")
            m3.metric("Simulated Logical Qubits", f"{res['qubit_count']}")

            st.markdown("#### 📜 Execution Trace Diagram")
            st.code("\n".join(res.get("execution_steps", [])), language="text")


# ==============================================================================
# TAB 4: GROVER LABORATORY
# ==============================================================================
elif lab_choice == "🔍 Grover Key Search Laboratory":
    st.markdown("### 🔍 Grover's Algorithm Quadratic Preimage Search")
    st.markdown("""
    <div class='notice-box'>
    <b>Algorithmic Complexity Demonstration:</b> Compares classical linear search \\(O(N)\\) 
    against Grover quantum amplitude amplification \\(O(\\sqrt{N})\\) for preimage and key space search.
    </div>
    """, unsafe_allow_html=True)

    k_bits = st.slider("Search Space Bit Length (k):", 4, 12, 8)
    res = run_grover_search_analysis(key_space_bits=k_bits)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Search Space Size (N)", f"{res['search_space_size_N']:,}")
    c2.metric("Classical Avg Attempts", f"{res['classical_avg_attempts']:,}")
    c3.metric("Grover Iterations", f"{res['grover_iterations']}")
    c4.metric("Algorithmic Speedup", f"{res['speedup_factor']}x")

    # Trace Chart
    df_trace = pd.DataFrame(res["amplitude_trace"])
    fig = px.line(
        df_trace, 
        x="iteration", 
        y="target_probability",
        title=f"Grover Probability Amplification Across Iterations (N={res['search_space_size_N']})",
        markers=True,
        line_shape="spline"
    )
    fig.update_traces(line_color="#3fb950", line_width=3)
    fig.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", font_color="#c9d1d9")
    st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# TAB 5: PQC COMPARISON
# ==============================================================================
elif lab_choice == "📜 Post-Quantum (PQC) Comparison":
    st.markdown("### 📜 Post-Quantum Cryptography (PQC) vs Classical Benchmarking")
    st.markdown("""
    <div class='notice-box'>
    <b>NIST FIPS 204 / 205 Standards:</b> Evaluates ML-DSA (Module-Lattice) and SLH-DSA (Stateless Hash-based) 
    signature overheads against classical ECDSA P-256 and RSA-2048.
    </div>
    """, unsafe_allow_html=True)

    pqc_schemes = list_pqc_schemes()
    selected_pqc = st.selectbox("Select NIST PQC Scheme:", pqc_schemes, index=0)
    meta = get_pqc_scheme_metadata(selected_pqc)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Public Key Size", f"{meta['public_key_bytes']} bytes", f"{meta['pubkey_overhead_vs_ecdsa']}x vs ECDSA")
    c2.metric("Signature Size", f"{meta['signature_bytes']} bytes", f"{meta['sig_overhead_vs_ecdsa']}x vs ECDSA")
    c3.metric("NIST Security Category", f"Category {meta['nist_security_category']}")
    c4.metric("Quantum Classification", f"{meta['quantum_threat_classification']}")

    st.markdown("#### 🔬 Comprehensive Overhead Comparison Matrix")
    df_comp = pd.DataFrame([
        {"Scheme": "ECDSA-P256", "Type": "Classical", "Public Key (B)": 64, "Signature (B)": 64, "Quantum Status": "Vulnerable"},
        {"Scheme": "RSA-2048", "Type": "Classical", "Public Key (B)": 256, "Signature (B)": 256, "Quantum Status": "Vulnerable"},
        {"Scheme": "ML-DSA-44", "Type": "PQC Lattice", "Public Key (B)": 1312, "Signature (B)": 2420, "Quantum Status": "Resistant"},
        {"Scheme": "ML-DSA-65", "Type": "PQC Lattice", "Public Key (B)": 1952, "Signature (B)": 3309, "Quantum Status": "Resistant"},
        {"Scheme": "SLH-DSA-128f", "Type": "PQC Hash", "Public Key (B)": 32, "Signature (B)": 17088, "Quantum Status": "Resistant"},
    ])
    st.table(df_comp)


# ==============================================================================
# TAB 6: UNIFIED RISK ASSESSMENT
# ==============================================================================
elif lab_choice == "📊 Unified Quantum Risk Assessment":
    st.markdown("### 📊 Unified Deterministic Quantum Risk Engine")
    st.markdown("""
    <div class='notice-box'>
    <b>Mosca Theorem Risk Engine (Zero AI/ML):</b> Computes risk classification by combining 
    mathematical quantum vulnerability, CRQC resource requirements, and data lifecycle horizons (\\(X + Y > Z\\)).
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        alg = st.selectbox("Target Digital Signature Algorithm:", ["RSA-2048", "RSA-4096", "ECDSA-P256", "Ed25519", "ML-DSA-44", "QDS-Teleportation"], index=0)
        x_years = st.slider("Data Retention Requirement (X years):", 1, 30, 10)
        y_years = st.slider("Infrastructure Migration Time (Y years):", 1, 15, 5)

    with col2:
        risk_res = evaluate_quantum_risk(algorithm_name=alg, data_retention_years=x_years, infrastructure_lifecycle_years=y_years)
        
        lvl = risk_res["risk_level"]
        if lvl == "CRITICAL":
            st.error(f"🚨 UNIFIED QUANTUM RISK LEVEL: {lvl} (Score: {risk_res['overall_risk_score_100']}/100)")
        elif lvl == "HIGH":
            st.warning(f"⚠️ UNIFIED QUANTUM RISK LEVEL: {lvl} (Score: {risk_res['overall_risk_score_100']}/100)")
        else:
            st.success(f"✅ UNIFIED QUANTUM RISK LEVEL: {lvl} (Score: {risk_res['overall_risk_score_100']}/100)")

        st.markdown(f"**Action Recommendation:** {risk_res['action_recommendation']}")
        st.markdown(f"**Mosca Threshold Formula:** `{risk_res['mosca_theorem_analysis']['formula_status']}`")

        if risk_res["resource_estimates"]["logical_qubits_required"] > 0:
            st.markdown(f"<div style='background-color: rgba(56, 139, 253, 0.15); border-left: 4px solid #58a6ff; padding: 12px; border-radius: 4px;'>"
                        f"<b>Estimated CRQC Logical Qubits:</b> {risk_res['resource_estimates']['logical_qubits_required']:,} | "
                        f"<b>Physical Surface Code Qubits:</b> {risk_res['resource_estimates']['physical_qubits_required']:,}</div>", unsafe_allow_html=True)
