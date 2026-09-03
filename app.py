"""
Q-Sentinel: Quantum-Statistical Threat Detection for Teleportation-Based Digital Signatures.
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

from qds_detector.config import ExperimentConfig, SessionContext, ThresholdConfig
from qds_detector.states import PAULI_STATES, STATE_ALIASES, get_expected_probabilities
from qds_detector.protocol import run_qds_experiment


# Page Configuration
st.set_page_config(
    page_title="Q-Sentinel | Quantum Digital Signature Security Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Hero Cards and Security Laboratory Theme
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
    .hero-title-accept {
        color: #3fb950;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .hero-title-reject {
        color: #f85149;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .hero-title-suspicious {
        color: #e3b341;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
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
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.title("🛡️ Q-SENTINEL")
st.markdown("### Quantum-Statistical Threat Detection for Teleportation-Based Digital Signatures")
st.markdown("""
<span class="badge-no-ai">SIH26141 • EGREEN QUANTA</span> &nbsp;&nbsp;
<span style="color:#8b949e; font-size:14px;">Deterministic Quantum Hypothesis Testing • Basis-Calibrated • Strictly NO AI/ML</span>
""", unsafe_allow_html=True)
st.divider()

# Sidebar Control Panel
st.sidebar.header("🔬 Protocol Experiment Setup")

# 1. Quantum State Selection
input_state = st.sidebar.selectbox(
    "Input Signature State (|ψ⟩)",
    options=["|0>", "|1>", "|+>", "|->", "|+i>", "|-i>"],
    index=4,  # Default to |+i>
    help="Select one of 6 Pauli basis eigenstates."
)

# 2. Measurement Basis Selection
basis_options = {"Y (Phase Basis)": "Y", "Z (Computational)": "Z", "X (Hadamard)": "X"}
basis_label = st.sidebar.selectbox("Verification Measurement Basis", options=list(basis_options.keys()), index=0)
measurement_basis = basis_options[basis_label]

# 3. Shot Count
shots = st.sidebar.slider("Measurement Shot Count (N)", min_value=1000, max_value=10000, value=5000, step=500)

st.sidebar.divider()
st.sidebar.header("⚔️ Threat & Attack Injection")

attack_type_map = {
    "None (Legitimate Signature)": "none",
    "State Forgery (Quantum State Perturbation)": "forgery",
    "Channel Manipulation (Depolarizing Noise)": "channel_depolarizing",
    "Channel Manipulation (Bit-Flip Noise)": "channel_bit_flip",
    "Channel Manipulation (Phase-Flip Noise)": "channel_phase_flip",
    "Replay Attack (Stale Nonce / Session Reuse)": "replay",
    "Impersonation Attack (Unauthorized Signer ID)": "impersonation"
}

selected_attack_label = st.sidebar.selectbox("Attack Scenario", options=list(attack_type_map.keys()), index=0)
attack_type = attack_type_map[selected_attack_label]

if attack_type not in ["none", "replay", "impersonation"]:
    attack_severity = st.sidebar.slider("Attack Severity (λ)", min_value=0.0, max_value=1.0, value=0.65, step=0.05)
else:
    attack_severity = 0.0

st.sidebar.divider()
st.sidebar.header("⚙️ Detector Calibration Settings")

alpha = st.sidebar.number_input("Significance Level (α)", min_value=0.001, max_value=0.05, value=0.01, step=0.001, format="%.3f")
min_fidelity_accept = st.sidebar.number_input("Min Fidelity Threshold", min_value=0.80, max_value=1.00, value=0.98, step=0.01)

thresholds = ThresholdConfig(
    shots=shots,
    alpha=alpha,
    min_fidelity_accept=min_fidelity_accept
)

# Build & Run Experiment
exp_config = ExperimentConfig(
    input_state=input_state,
    measurement_basis=measurement_basis,
    shots=shots,
    seed=42,
    attack_type=attack_type,
    attack_severity=attack_severity,
    thresholds=thresholds
)

exp_record = run_qds_experiment(exp_config)

# Main Dashboard Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Hero Verification Lab",
    "📈 Attack Sensitivity Benchmark",
    "📐 Two-Tier Architecture & Math",
    "📄 Reproducibility & Record Exporter"
])

# ---------------------------------------------------------
# TAB 1: Hero Verification Lab
# ---------------------------------------------------------
with tab1:
    decision = exp_record["decision"]
    reason = exp_record["reason"]
    evidence = exp_record["evidence"]
    tier1 = evidence.get("tier1_protocol", {})
    tier2 = evidence.get("tier2_quantum", {})
    threat_cat = exp_record.get("threat_category", "NONE")

    # Hero Callout Card
    if decision == "ACCEPT":
        st.markdown(f"""
        <div class="hero-accept">
            <div class="hero-title-accept">🟢 SIGNATURE VALIDATED</div>
            <div style="color: #8b949e; font-size: 16px;">{reason}</div>
        </div>
        """, unsafe_allow_html=True)
    elif decision == "SUSPICIOUS":
        st.markdown(f"""
        <div class="hero-suspicious">
            <div class="hero-title-suspicious">⚠️ SIGNATURE SUSPICIOUS</div>
            <div style="color: #8b949e; font-size: 16px;">{reason}</div>
            <div class="hero-threat-tag">POTENTIAL THREAT: {threat_cat}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="hero-reject">
            <div class="hero-title-reject">🔴 SIGNATURE REJECTED</div>
            <div style="color: #8b949e; font-size: 16px;">{reason}</div>
            <div class="hero-threat-tag">DETECTED THREAT: {threat_cat}</div>
        </div>
        """, unsafe_allow_html=True)

    # Verification Metrics Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Fidelity F", f"{exp_record['fidelity']:.4f}")
    m2.metric("Prob Deviation Δ", f"{exp_record['deviation']:.4f}")
    m3.metric("z-score", f"{exp_record['z_score']:.2f}")
    m4.metric("p-value", f"{exp_record['p_value']:.4e}")
    m5.metric("Freshness", "VALID" if exp_record['freshness_valid'] else "STALE ❌")
    m6.metric("Identity", "VALID" if exp_record['identity_valid'] else "MISMATCH ❌")

    st.divider()

    # Two-Tier Architecture Breakdown
    c_tier1, c_tier2 = st.columns(2)

    with c_tier1:
        st.markdown("#### 🔒 Tier 1: Protocol Context Layer")
        fresh_status = "🟢 Passed (Nonce Active)" if exp_record['freshness_valid'] else "🔴 Failed (Nonce Stale / Replayed)"
        ident_status = "🟢 Passed (Signer Key Verified)" if exp_record['identity_valid'] else "🔴 Failed (Signer Key Mismatch)"
        
        st.markdown(f"""
        <div class="tier-box">
            <b>Freshness Verification</b>: {fresh_status}<br>
            <b>Session ID</b>: <code>{exp_config.session_context.session_id}</code><br>
            <b>Signer Identity Verification</b>: {ident_status}<br>
            <b>Signer Key ID</b>: <code>{exp_config.session_context.signer_id}</code>
        </div>
        """, unsafe_allow_html=True)

    with c_tier2:
        st.markdown("#### ⚛️ Tier 2: Quantum Statistics Layer")
        max_thresh = thresholds.get_max_deviation_accept(measurement_basis)
        dev_status = "🟢 Within Threshold" if exp_record['deviation'] <= max_thresh else "🔴 Threshold Exceeded"
        
        st.markdown(f"""
        <div class="tier-box">
            <b>Verification Basis</b>: <code>{measurement_basis}</code><br>
            <b>Basis Calibrated Threshold</b>: Max Δ ≤ <b>{max_thresh:.4f}</b> ({dev_status})<br>
            <b>State Fidelity F(ρ_in, ρ_out)</b>: <b>{exp_record['fidelity']:.4f}</b><br>
            <b>Chi-Square Statistic χ²</b>: <b>{tier2.get('chi2_statistic', 0.0):.4f}</b>
        </div>
        """, unsafe_allow_html=True)

    # Outcome Histogram Plot
    st.subheader("📊 Projective Outcome Probability Distribution")
    obs_p = exp_record["observed_probability"]
    base_p = exp_record["baseline_probability"]
    
    df_plot = pd.DataFrame({
        "Outcome": ["+1 Eigenstate", "-1 Eigenstate"],
        "Observed Probability": [obs_p.get("+1", 0), obs_p.get("-1", 0)],
        "Expected Baseline": [base_p.get("+1", 0), base_p.get("-1", 0)]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot["Outcome"],
        y=df_plot["Observed Probability"],
        name="Observed (Empirical Shots)",
        marker_color="#388bfd"
    ))
    fig.add_trace(go.Bar(
        x=df_plot["Outcome"],
        y=df_plot["Expected Baseline"],
        name="Legitimate Baseline",
        marker_color="#2ea043"
    ))
    fig.update_layout(
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: Attack Sensitivity Benchmark
# ---------------------------------------------------------
with tab2:
    st.subheader("📈 Multi-Trial Attack Sensitivity Benchmark")
    st.markdown("Evaluates detector response across increasing attack severity $\lambda$ without single-point bias.")
    
    sweep_attack = st.selectbox(
        "Select Attack Vector for Sweep",
        options=["forgery", "channel_depolarizing", "channel_bit_flip", "channel_phase_flip"],
        index=0
    )
    
    severities = np.linspace(0.0, 1.0, 21)
    sweep_records = []
    
    for sev in severities:
        cfg = ExperimentConfig(
            input_state=input_state,
            measurement_basis=measurement_basis,
            shots=shots,
            seed=42,
            attack_type=sweep_attack,
            attack_severity=float(sev),
            thresholds=thresholds
        )
        rec = run_qds_experiment(cfg)
        sweep_records.append({
            "severity": float(sev),
            "decision": rec["decision"],
            "fidelity": rec["fidelity"],
            "deviation": rec["deviation"],
            "p_value": rec["p_value"]
        })
        
    df_sweep = pd.DataFrame(sweep_records)
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_fid = px.line(
            df_sweep, x="severity", y="fidelity",
            title="State Fidelity F(ρ_in, ρ_out) vs Attack Severity λ",
            labels={"severity": "Attack Severity λ", "fidelity": "Fidelity F"},
            template="plotly_dark"
        )
        fig_fid.add_hline(y=min_fidelity_accept, line_dash="dash", line_color="#3fb950", annotation_text="Min Accept Threshold")
        fig_fid.update_traces(line_color="#f85149", line_width=3)
        fig_fid.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", height=320)
        st.plotly_chart(fig_fid, use_container_width=True)
        
    with c2:
        fig_dev = px.line(
            df_sweep, x="severity", y="deviation",
            title=f"Basis {measurement_basis} Probability Deviation Δ vs Severity λ",
            labels={"severity": "Attack Severity λ", "deviation": "Probability Deviation Δ"},
            template="plotly_dark"
        )
        max_t = thresholds.get_max_deviation_accept(measurement_basis)
        fig_dev.add_hline(y=max_t, line_dash="dash", line_color="#3fb950", annotation_text=f"Max Δ Threshold ({max_t})")
        fig_dev.update_traces(line_color="#d29922", line_width=3)
        fig_dev.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", height=320)
        st.plotly_chart(fig_dev, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: Two-Tier Architecture & Math Inspector
# ---------------------------------------------------------
with tab3:
    st.subheader("📐 Two-Tier Architecture & Scientific Methodology")
    
    st.info("""
    **Core Design Principle (SIH Defense)**:  
    The problem specification requires a quantum-principle-based detector without AI/ML. Our approach therefore uses directly interpretable measurement statistics, calibrated confidence bounds and deterministic hypothesis-testing rules. Every decision can be traced back to an observable quantum measurement rather than a learned model.
    """)
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.markdown("#### Tier 1: Protocol Context Layer")
        st.markdown("""
        - **Identity Verification**: Checks presented signer public key against expected context. Traps **Impersonation Attacks**.
        - **Freshness Verification**: Validates unique challenge nonces and session timestamps. Traps **Replay Attacks**.
        """)
        
    with col_m2:
        st.markdown("#### Tier 2: Quantum Measurement Layer")
        st.latex(r"P_\pm = \frac{I \pm \sigma}{2}, \quad p_\pm = \mathrm{Tr}(P_\pm \rho), \quad \sigma \in \{X, Y, Z\}")
        st.latex(r"z = \frac{\hat{p} - p_0}{SE}, \quad \chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}")
        st.markdown("""
        - Evaluates projective outcome probabilities $\hat{p}_\pm$ against basis-calibrated baseline expectations $p_0$.
        - Traps **State Forgery** and **Quantum Channel Noise**.
        """)

# ---------------------------------------------------------
# TAB 4: Reproducibility & Record Exporter
# ---------------------------------------------------------
with tab4:
    st.subheader("📄 Reproducibility Record (Appendix A Standard)")
    json_str = json.dumps(exp_record, indent=2)
    st.code(json_str, language="json")
    
    st.download_button(
        label="📥 Download Experiment Record JSON",
        data=json_str,
        file_name=f"{exp_record['experiment_id']}.json",
        mime="application/json"
    )
