"""
Training & ONNX Export Pipeline for Edge Threat Classifier.
SIH26141 • Egreen Quanta
"""

import os
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

from qds_detector.edge_ai.dataset_generator import generate_synthetic_dataset, LABEL_MAP
from qds_detector.edge_ai.features import extract_batch_features


def train_and_export_model(
    output_dir: str | None = None,
    num_samples: int = 900,
    seed: int = 42
) -> str:
    """
    Trains a lightweight Random Forest threat classifier on synthetic telemetry,
    exports model to joblib and ONNX if skl2onnx is available, or saves serializable tree weights.
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    
    os.makedirs(output_dir, exist_ok=True)
    
    events, labels = generate_synthetic_dataset(num_samples=num_samples, seed=seed)
    X = extract_batch_features(events)
    y = np.array(labels, dtype=int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)

    clf = RandomForestClassifier(n_estimators=30, max_depth=8, random_state=seed)
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(f"[Edge AI Train] Random Forest Classifier Accuracy: {score * 100:.2f}%")

    model_path = os.path.join(output_dir, "q_sentinel_classifier.joblib")
    joblib.dump(clf, model_path)

    # Try ONNX Export if skl2onnx is installed
    onnx_path = os.path.join(output_dir, "q_sentinel_threat_classifier.onnx")
    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        initial_type = [('float_input', FloatTensorType([None, 12]))]
        onx = convert_sklearn(clf, initial_types=initial_type)
        with open(onnx_path, "wb") as f:
            f.write(onx.SerializeToString())
        print(f"[Edge AI Train] Exported ONNX model to: {onnx_path}")
    except Exception as e:
        print(f"[Edge AI Train] skl2onnx conversion skipped ({e}). Joblib model saved to {model_path}.")

    return model_path


if __name__ == "__main__":
    train_and_export_model()
