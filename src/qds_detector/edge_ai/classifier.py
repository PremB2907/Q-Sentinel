"""
Local ONNX-Backed Edge Threat Classifier for Q-Sentinel Edge.
SIH26141 • Egreen Quanta
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import numpy as np
import joblib

from qds_detector.edge_ai.schema import SecurityEvent
from qds_detector.edge_ai.features import extract_feature_vector
from qds_detector.snapdragon.runtime import get_onnx_runtime_session, SnapdragonRuntimeManager


class EdgeThreatClassifier:
    """
    On-device threat classifier that uses ONNX Runtime / QNN execution provider
    or scikit-learn joblib fallback to evaluate structured telemetry.
    """
    def __init__(self, model_dir: Optional[str] = None):
        if model_dir is None:
            model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
        
        self.model_dir = model_dir
        self.onnx_path = os.path.join(model_dir, "q_sentinel_threat_classifier.onnx")
        self.joblib_path = os.path.join(model_dir, "q_sentinel_classifier.joblib")
        
        self.runtime_mgr = SnapdragonRuntimeManager()
        self.ort_session = None
        self.joblib_clf = None

        self._load_model()

    def _load_model(self):
        """Attempts to load ONNX Runtime session first, fallback to Joblib model if ONNX missing."""
        if os.path.exists(self.onnx_path):
            self.ort_session, self.active_provider = self.runtime_mgr.create_session(self.onnx_path)
            if self.ort_session is not None:
                return

        if os.path.exists(self.joblib_path):
            self.joblib_clf = joblib.load(self.joblib_path)
            self.active_provider = "Scikit-Learn Joblib Fallback (CPU)"
        else:
            # Train a quick fallback model if not found
            from qds_detector.edge_ai.train import train_and_export_model
            train_and_export_model(output_dir=self.model_dir)
            if os.path.exists(self.joblib_path):
                self.joblib_clf = joblib.load(self.joblib_path)
            self.active_provider = "CPU (Auto-Trained Fallback)"

    def predict(self, event: SecurityEvent) -> Dict[str, Any]:
        """
        Runs local inference on a SecurityEvent instance.

        Returns:
            Dictionary containing:
            - classification: "NORMAL", "SUSPICIOUS", "ATTACK"
            - confidence_scores: Dict mapping class names to probabilities
            - execution_provider: Name of active execution provider (QNN/NPU, DirectML, CPU)
            - inference_latency_ms: Microsecond-precision inference time
        """
        import time
        start = time.perf_counter()

        feats = extract_feature_vector(event).reshape(1, -1)
        classes = ["NORMAL", "SUSPICIOUS", "ATTACK"]

        if self.ort_session is not None:
            input_name = self.ort_session.get_inputs()[0].name
            outputs = self.ort_session.run(None, {input_name: feats})
            
            # ORT tree output format: [label_array, [{class_id: prob}]]
            if len(outputs) >= 2 and isinstance(outputs[1], list):
                prob_dict = outputs[1][0]
                probs = [prob_dict.get(0, 0.0), prob_dict.get(1, 0.0), prob_dict.get(2, 0.0)]
            else:
                pred_idx = int(outputs[0][0])
                probs = [0.0, 0.0, 0.0]
                probs[pred_idx] = 1.0
        elif self.joblib_clf is not None:
            probs = self.joblib_clf.predict_proba(feats)[0]
        else:
            # Deterministic heuristic fallback
            if not event.nonce_valid or not event.signer_valid or event.fidelity < 0.85:
                probs = [0.05, 0.15, 0.80]
            elif event.probability_deviation > 0.08:
                probs = [0.10, 0.70, 0.20]
            else:
                probs = [0.90, 0.08, 0.02]

        elapsed_ms = (time.perf_counter() - start) * 1000.0

        max_idx = int(np.argmax(probs))
        classification = classes[max_idx]

        conf_dict = {
            "NORMAL": round(float(probs[0]), 4),
            "SUSPICIOUS": round(float(probs[1]), 4),
            "ATTACK": round(float(probs[2]), 4)
        }

        return {
            "classification": classification,
            "confidence_scores": conf_dict,
            "top_confidence": round(float(probs[max_idx]), 4),
            "execution_provider": getattr(self, "active_provider", "CPU"),
            "inference_latency_ms": round(elapsed_ms, 3)
        }


# Singleton default classifier instance
_DEFAULT_CLASSIFIER: Optional[EdgeThreatClassifier] = None

def get_default_classifier() -> EdgeThreatClassifier:
    global _DEFAULT_CLASSIFIER
    if _DEFAULT_CLASSIFIER is None:
        _DEFAULT_CLASSIFIER = EdgeThreatClassifier()
    return _DEFAULT_CLASSIFIER
