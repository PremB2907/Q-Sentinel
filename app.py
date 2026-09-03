"""
Q-Sentinel: Quantum-Inspired Cyber Threat Detection for Digital Signature Security (SIH26141).
Streamlit Dashboard Laboratory Interface.
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
from qds_detector.attacks import simulate_attack_counts, apply_forgery_attack, apply_channel_attack
from qds_detector.detector import evaluate_threat_detection
from qds_detector.metrics import compute_batch_metrics


# Page Configuration
st.set_page_config(
    page_title="Q-Sentinel | QDS Threat Detection Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyber-Security Laboratory Theme
st.markdown("""
<style>
    /* Dark Cyber Theme Adjustments */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .css-1d37w0k {
        background-color: #161b22;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .decision-accept {
        background-color: rgba(46, 160, 67, 0.15);
        border: 2px solid #2ea043;
        color: #3fb950;
        padding: 16px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .decision-suspicious {
        background-color: rgba(210, 153, 34, 0.15);
        border: 2px solid #d29922;
        color: #e3b341;
        padding: 16px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .decision-reject {
        background-color: rgba(248, 81, 73, 0.15);
        border: 2px solid #f85149;
        color: #f85149;
        padding: 16px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
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
st.markdown("### Quantum-Inspired Cyber Threat Detection for Digital Signature Security")
st.markdown("""
<span class="badge-no-ai">SIH26141 • EGREEN QUANTA</span> &nbsp;&nbsp;
<span style="color:#8b949e; font_size:14px;">Rule-Based Quantum Statistical Detector • Strictly NO AI/ML</span>
""", unsafe_allow_html=True)
st.divider()

# Sidebar Control Panel
st.sidebar.header("🔬 Experiment Control Panel")

# 1. Quantum State Selection
input_state = st.sidebar.selectbox(
    "Input Signature / Test Qubit State",
    options=["|0>", "|1>", "|+>", "|->", "|+i>", "|-i>"],
    index=0,
    help="Select one of 6 Pauli basis eigenstates."
)

# 2. Measurement Basis Selection
basis_options = {"Z (Computational)": "Z", "X (Hadamard)": "X", "Y (Phase)": "Y"}
basis_label = st.sidebar.selectbox(
    "Verification Measurement Basis",
    options=list(basis_options.keys()),
    index=0
)
measurement_basis = basis_options[basis_label]

# 3. Shot Count
shots = st.sidebar.slider("Number of Measurement Shots (N)", min_value=1000, max_value=10000, value=5000, step=500)

st.sidebar.divider()
st.sidebar.header("⚔️ Threat & Attack Injection")

attack_type_map = {
    "None (Legitimate Teleportation)": "none",
    "State Forgery (State Perturbation)": "forgery",
    "Channel Manipulation (Bit-Flip Noise)": "channel_bit_flip",
    "Channel Manipulation (Phase-Flip Noise)": "channel_phase_flip",
    "Channel Manipulation (Depolarizing Noise)": "channel_depolarizing",
    "Replay Attack (Stale Nonce / Transcript Reuse)": "replay",
    "Impersonation Attack (Unauthorized Signer ID)": "impersonation"
}

selected_attack_label = st.sidebar.selectbox("Attack Scenario", options=list(attack_type_map.keys()), index=0)
attack_type = attack_type_map[selected_attack_label]

if attack_type not in ["none", "replay", "impersonation"]:
    attack_severity = st.sidebar.slider("Attack Severity (λ / Noise Probability)", min_value=0.0, max_value=1.0, value=0.35, step=0.05)
else:
    attack_severity = 0.0

st.sidebar.divider()
st.sidebar.header("⚙️ Calibrated Detector Thresholds")

alpha = st.sidebar.number_input("Significance Level (α)", min_value=0.001, max_value=0.05, value=0.01, step=0.001, format="%.3f")
min_fidelity_accept = st.sidebar.number_input("Min Fidelity Accept", min_value=0.80, max_value=1.00, value=0.98, step=0.01)
max_dev_accept = st.sidebar.number_input("Max Probability Dev Accept", min_value=0.01, max_value=0.10, value=0.03, step=0.005)

thresholds = ThresholdConfig(
    shots=shots,
    alpha=alpha,
    min_fidelity_accept=min_fidelity_accept,
    max_probability_deviation_accept=max_dev_accept,
    min_fidelity_suspicious=0.90,
    max_probability_deviation_suspicious=0.10
)

# Run Button
run_experiment = st.sidebar.button("⚡ Run Quantum Teleportation & Verification", type="primary", use_container_width=True)

# Build Experiment Configuration
exp_config = ExperimentConfig(
    input_state=input_state,
    measurement_basis=measurement_basis,
    shots=shots,
    seed=42,
    attack_type=attack_type,
    attack_severity=attack_severity,
    thresholds=thresholds
)

# Execute Experiment
exp_record = run_qds_experiment(exp_config)

# Main Dashboard Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Live Laboratory & Detector",
    "📈 Attack Strength Sensitivity Sweep",
    "📐 Statistical Model & Physics Inspector",
    "📄 Reproducibility & Record Exporter"
])

# ---------------------------------------------------------
# TAB 1: Live Verification Lab & Threat Detector
# ---------------------------------------------------------
with tab1:
    col_dec, col_meta = st.columns([1.2, 1.8])
    
    with col_dec:
        decision = exp_record["decision"]
        reason = exp_record["reason"]
        
        if decision == "ACCEPT":
            st.markdown(f'<div class="decision-accept">✅ DECISION: ACCEPT</div>', unsafe_allow_html=True)
        elif decision == "SUSPICIOUS":
            st.markdown(f'<div class="decision-suspicious">⚠️ DECISION: SUSPICIOUS</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="decision-reject">❌ DECISION: REJECT</div>', unsafe_allow_html=True)
            
        st.markdown(f"**Rationale**: {reason}")
        
    with col_meta:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("State Fidelity F", f"{exp_record['fidelity']:.4f}")
        m2.metric("Prob Deviation", f"{exp_record['deviation']:.4f}")
        m3.metric("z-score", f"{exp_record['z_score']:.2f}")
        m4.metric("p-value", f"{exp_record['p_value']:.4e}")
        
        st.caption(f"⏱️ Teleportation + Analysis Latency: **{exp_record['execution_time_ms']:.2f} ms** | Shots: **{exp_record['shots']}**")

    st.divider()
    
    # Live Measurement Plots
    col_chart, col_circuit = st.columns([1.5, 1.0])
    
    with col_chart:
        st.subheader("📊 Quantum Measurement Outcome Distribution")
        
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

    with col_circuit:
        st.subheader("🌀 3-Qubit Teleportation Protocol")
        st.markdown(f"""
        - **Input State**: `{input_state}` initialized on $q_0$
        - **Entangled Bell Pair**: $|\Phi^+\rangle = \\frac{{|00\\rangle + |11\\rangle}}{{\\sqrt{{2}}}}$ on $(q_1, q_2)$
        - **Bell Measurement**: Applied on $(q_0, q_1)$
        - **Pauli Corrections**: Conditional $X/Z$ applied on receiver $q_2$
        - **Verification Basis**: `{measurement_basis}`-basis projection on $q_2$
        """)
        
        st.info(f"""
        **Protocol Context**:
        - Freshness / Nonce Valid: **{exp_record['freshness_valid']}**
        - Signer Identity Match: **{exp_record['identity_valid']}**
        """)

# ---------------------------------------------------------
# TAB 2: Attack Severity Sensitivity Sweep
# ---------------------------------------------------------
with tab2:
    st.subheader("📈 Attack Severity Sensitivity Sweep (0.0 to 1.0)")
    st.markdown("Evaluates detector response across increasing attack severity $\lambda$ without cherry-picking single data points.")
    
    sweep_attack = st.selectbox(
        "Select Attack for Sweep",
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
            "p_value": rec["p_value"],
            "rejected": 1 if rec["decision"] in ["REJECT", "SUSPICIOUS"] else 0,
            "false_accept": 1 if (sev > 0.1 and rec["decision"] == "ACCEPT") else 0
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
            title="Probability Deviation max|p_obs - p_base| vs Attack Severity λ",
            labels={"severity": "Attack Severity λ", "deviation": "Probability Deviation"},
            template="plotly_dark"
        )
        fig_dev.add_hline(y=max_dev_accept, line_dash="dash", line_color="#3fb950", annotation_text="Max Accept Threshold")
        fig_dev.update_traces(line_color="#d29922", line_width=3)
        fig_dev.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", height=320)
        st.plotly_chart(fig_dev, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: Statistical Model & Physics Inspector
# ---------------------------------------------------------
with tab3:
    st.subheader("📐 Mathematical & Statistical Foundation")
    
    col_math1, col_math2 = st.columns(2)
    
    with col_math1:
        st.markdown("#### 1. Pauli Projective Measurements")
        st.latex(r"P_+ = \frac{I + \sigma}{2}, \quad P_- = \frac{I - \sigma}{2}, \quad \sigma \in \{X, Y, Z\}")
        st.latex(r"p_\pm = \mathrm{Tr}(P_\pm \rho)")
        st.markdown("Verification probabilities are evaluated directly from quantum projection operators without feeding raw states into learned ML models.")
        
    with col_math2:
        st.markdown("#### 2. Hypothesis Testing & z-Score")
        st.latex(r"\hat{p} = \frac{k}{N}, \quad SE = \sqrt{\frac{p_0 (1-p_0)}{N}}")
        st.latex(r"z = \frac{\hat{p} - p_0}{SE}, \quad p\text{-value} = 2(1 - \Phi(|z|))")
        st.markdown("Observed counts $k$ are compared against calibrated baseline expected probability $p_0$ under standard normal distribution bounds.")

# ---------------------------------------------------------
# TAB 4: Reproducibility & Record Exporter
# ---------------------------------------------------------
with tab4:
    st.subheader("📄 Experiment Record (Appendix A Specification)")
    st.markdown("Reproducible experiment transcript exported as structured JSON matching SIH26141 blueprint standard.")
    
    json_str = json.dumps(exp_record, indent=2)
    st.code(json_str, language="json")
    
    st.download_button(
        label="📥 Download Experiment Record JSON",
        data=json_str,
        file_name=f"{exp_record['experiment_id']}.json",
        mime="application/json"
    )
