"""
Empirical Latency & Throughput Benchmarker for Edge AI Runtime.
SIH26141 • Egreen Quanta
Qualcomm Snapdragon AI Lab Challenge
"""

import time
import numpy as np
from typing import Dict, Any
from qds_detector.edge_ai.schema import SecurityEvent
from qds_detector.edge_ai.features import extract_feature_vector


def run_edge_benchmark(num_iterations: int = 100, warmup_iterations: int = 10) -> Dict[str, Any]:
    """
    Measures actual empirical preprocessing latency, model inference latency,
    end-to-end latency, percentiles (p50, p90, p99), throughput, and active execution provider metrics.
    """
    from qds_detector.edge_ai.classifier import get_default_classifier
    classifier = get_default_classifier()
    
    dummy_event = SecurityEvent(
        fidelity=0.92,
        probability_deviation=0.04,
        z_score=1.85,
        p_value=0.02,
        chi2_statistic=4.2,
        signer_valid=True,
        nonce_valid=True,
        session_valid=True
    )

    # Warmup runs
    for _ in range(warmup_iterations):
        _ = classifier.predict(dummy_event)

    # Benchmark loop
    preprocess_latencies = []
    inference_latencies = []
    e2e_latencies = []

    start_total = time.perf_counter()
    
    for _ in range(num_iterations):
        t_start = time.perf_counter()
        
        # Preprocessing time
        t_prep_0 = time.perf_counter()
        feats = extract_feature_vector(dummy_event)
        t_prep_ms = (time.perf_counter() - t_prep_0) * 1000.0
        preprocess_latencies.append(t_prep_ms)

        # Full prediction (includes inference)
        res = classifier.predict(dummy_event)
        t_e2e_ms = (time.perf_counter() - t_start) * 1000.0
        
        e2e_latencies.append(t_e2e_ms)
        inference_latencies.append(res.get("inference_latency_ms", t_e2e_ms))

    total_time_s = time.perf_counter() - start_total
    
    # Percentiles
    p50_e2e = float(np.percentile(e2e_latencies, 50))
    p90_e2e = float(np.percentile(e2e_latencies, 90))
    p99_e2e = float(np.percentile(e2e_latencies, 99))
    
    avg_inf = float(np.mean(inference_latencies))
    avg_prep = float(np.mean(preprocess_latencies))
    avg_e2e = float(np.mean(e2e_latencies))
    throughput = float(num_iterations / total_time_s)

    active_provider = res.get("execution_provider", "CPU")
    npu_status = "Hexagon NPU Active" if "QNN" in active_provider else "Snapdragon NPU execution: NOT YET VERIFIED (Requires Snapdragon Hardware)"

    return {
        "benchmark_iterations": num_iterations,
        "warmup_iterations": warmup_iterations,
        "active_execution_provider": active_provider,
        "snapdragon_npu_status": npu_status,
        "avg_latency_ms": round(avg_e2e, 4),
        "avg_preprocess_latency_ms": round(avg_prep, 4),
        "avg_inference_latency_ms": round(avg_inf, 4),
        "avg_e2e_latency_ms": round(avg_e2e, 4),
        "p50_e2e_latency_ms": round(p50_e2e, 4),
        "p90_e2e_latency_ms": round(p90_e2e, 4),
        "p99_e2e_latency_ms": round(p99_e2e, 4),
        "throughput_fps": round(throughput, 2),
        "model_name": "q_sentinel_threat_classifier.onnx",
        "input_shape": "[1, 11]",
        "model_architecture": "Compact MLP (11 -> 64 -> 32 -> 3)"
    }

