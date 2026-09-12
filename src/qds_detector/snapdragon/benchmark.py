"""
Empirical Latency & Throughput Benchmarker for Edge AI Runtime.
SIH26141 • Egreen Quanta
"""

import time
import numpy as np
from typing import Dict, Any
from qds_detector.edge_ai.schema import SecurityEvent
def run_edge_benchmark(num_iterations: int = 100, warmup_iterations: int = 10) -> Dict[str, Any]:
    """
    Measures actual empirical inference latency, throughput, and execution provider metrics.
    """
    from qds_detector.edge_ai.classifier import get_default_classifier
    classifier = get_default_classifier()
    dummy_event = SecurityEvent(
        fidelity=0.92,
        probability_deviation=0.04,
        z_score=1.85,
        p_value=0.02,
        chi2_statistic=4.2,
        attack_severity=0.20
    )

    # Warmup runs
    for _ in range(warmup_iterations):
        _ = classifier.predict(dummy_event)

    # Benchmark loop
    latencies = []
    start_total = time.perf_counter()
    
    for _ in range(num_iterations):
        t0 = time.perf_counter()
        res = classifier.predict(dummy_event)
        lat = (time.perf_counter() - t0) * 1000.0
        latencies.append(lat)

    total_time_s = time.perf_counter() - start_total
    avg_lat = float(np.mean(latencies))
    min_lat = float(np.min(latencies))
    p95_lat = float(np.percentile(latencies, 95))
    throughput = float(num_iterations / total_time_s)

    return {
        "benchmark_iterations": num_iterations,
        "warmup_iterations": warmup_iterations,
        "execution_provider": res["execution_provider"],
        "avg_latency_ms": round(avg_lat, 3),
        "min_latency_ms": round(min_lat, 3),
        "p95_latency_ms": round(p95_lat, 3),
        "throughput_fps": round(throughput, 2),
        "model_name": "q_sentinel_threat_classifier.onnx",
        "input_features": 12,
        "hardware_target": "Snapdragon-powered HP PC / Local Device"
    }
