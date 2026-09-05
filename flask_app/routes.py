"""
Q-Sentinel Flask Routes and REST API Blueprint.
SIH26141 • Egreen Quanta
"""

from flask import Blueprint, render_template, request, jsonify

# Domain A: QDS Core
from qds_detector.config import ExperimentConfig, SessionContext
from qds_detector.states import PAULI_STATES
from qds_detector.protocol import run_qds_experiment

# Domain B & C: Classical Threats, PQC & Risk Engine
from qds_detector.quantum_attacks.shor import run_shor_factorization
from qds_detector.quantum_attacks.ecc_analysis import analyze_ecc_dlog_threat
from qds_detector.quantum_attacks.grover import run_grover_search_analysis
from qds_detector.quantum_attacks.resource_estimator import estimate_crqc_resources
from qds_detector.quantum_attacks.pqc_analysis import get_pqc_scheme_metadata, list_pqc_schemes
from qds_detector.quantum_attacks.quantum_risk import evaluate_quantum_risk


main_bp = Blueprint("main", __name__)


# ==============================================================================
# HTML Page Routes
# ==============================================================================
@main_bp.route("/")
def index():
    """QDS Threat Lab Main Dashboard."""
    return render_template("qds_lab.html", pauli_states=list(PAULI_STATES.keys()))


@main_bp.route("/classical-threats")
def classical_threats():
    """Classical Digital Signature Quantum Threats Overview."""
    return render_template("classical_threats.html")


@main_bp.route("/shor")
def shor_lab():
    """Shor Factorization Laboratory."""
    return render_template("shor_lab.html")


@main_bp.route("/grover")
def grover_lab():
    """Grover Preimage Search Laboratory."""
    return render_template("grover_lab.html")


@main_bp.route("/pqc")
def pqc_lab():
    """Post-Quantum Cryptography Comparison Laboratory."""
    schemes = list_pqc_schemes()
    return render_template("pqc_lab.html", schemes=schemes)


@main_bp.route("/risk")
def risk_lab():
    """Unified Quantum Risk Assessment Engine."""
    return render_template("risk_lab.html")


# ==============================================================================
# REST API Endpoints
# ==============================================================================
@main_bp.route("/api/qds/run", methods=["POST"])
def api_qds_run():
    """Execute QDS Teleportation experiment endpoint."""
    data = request.get_json() or {}
    
    state_label = data.get("state_label", "|0>")
    basis_choice = data.get("basis", "Z")
    shots = int(data.get("shots", 1000))
    attack_type = data.get("attack_type", "clean")
    severity = float(data.get("severity", 0.0))

    ctx = SessionContext(
        nonce="valid_nonce_1001" if attack_type != "replay" else "expired_nonce_999",
        signer_id="Alice_PubKey_0x8F4A" if attack_type != "impersonation" else "Eve_Mallory",
        expected_signer_id="Alice_PubKey_0x8F4A"
    )

    config = ExperimentConfig(
        input_state=state_label,
        measurement_basis=basis_choice,
        shots=shots,
        attack_type=attack_type,
        attack_severity=severity,
        session_context=ctx
    )

    res = run_qds_experiment(config)
    return jsonify(res)


@main_bp.route("/api/shor/run", methods=["POST"])
def api_shor_run():
    """Run Shor factorization endpoint."""
    data = request.get_json() or {}
    N = int(data.get("N", 15))
    base_a = data.get("base_a")
    if base_a is not None:
        base_a = int(base_a)

    res = run_shor_factorization(N=N, base_a=base_a)
    return jsonify(res)


@main_bp.route("/api/grover/run", methods=["POST"])
def api_grover_run():
    """Run Grover search analysis endpoint."""
    data = request.get_json() or {}
    key_space_bits = int(data.get("key_space_bits", 8))
    
    res = run_grover_search_analysis(key_space_bits=key_space_bits)
    return jsonify(res)


@main_bp.route("/api/ecc/run", methods=["POST"])
def api_ecc_run():
    """Run ECC discrete log threat endpoint."""
    data = request.get_json() or {}
    curve_name = data.get("curve_name", "toy_p17")
    k = data.get("private_key_k")
    if k is not None:
        k = int(k)

    res = analyze_ecc_dlog_threat(curve_name=curve_name, private_key_k=k)
    return jsonify(res)


@main_bp.route("/api/pqc/scheme", methods=["GET"])
def api_pqc_scheme():
    """Get PQC scheme metadata endpoint."""
    name = request.args.get("name", "ML-DSA-44")
    res = get_pqc_scheme_metadata(name)
    return jsonify(res)


@main_bp.route("/api/risk/evaluate", methods=["POST"])
def api_risk_evaluate():
    """Evaluate quantum risk endpoint."""
    data = request.get_json() or {}
    alg = data.get("algorithm", "RSA-2048")
    x = int(data.get("x_years", 10))
    y = int(data.get("y_years", 5))

    res = evaluate_quantum_risk(algorithm_name=alg, data_retention_years=x, infrastructure_lifecycle_years=y)
    return jsonify(res)
