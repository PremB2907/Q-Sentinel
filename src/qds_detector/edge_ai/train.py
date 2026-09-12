"""
Training & ONNX Export Pipeline for Edge Threat Classifier.
SIH26141 • Egreen Quanta
Qualcomm Snapdragon AI Lab Challenge
"""

import os
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import joblib

from qds_detector.edge_ai.dataset_generator import generate_synthetic_dataset, LABEL_MAP
from qds_detector.edge_ai.features import extract_batch_features


def train_and_export_model(
    output_dir: str | None = None,
    num_samples: int = 1200,
    seed: int = 42
) -> str:
    """
    Trains a compact MLP threat classifier (11 -> 32 -> 16 -> 3) on synthetic telemetry,
    exports model to joblib and ONNX using standard matrix multiplication and ReLU operations.
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    
    os.makedirs(output_dir, exist_ok=True)
    
    events, labels = generate_synthetic_dataset(num_samples=num_samples, seed=seed)
    X = extract_batch_features(events)
    y = np.array(labels, dtype=int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)

    # Compact PyTorch-equivalent MLP: 11 inputs -> Hidden(64, ReLU) -> Hidden(32, ReLU) -> Output(3, Softmax)
    clf = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        learning_rate_init=0.005,
        max_iter=1000,
        random_state=seed
    )
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(f"[Edge AI Train] Compact MLP Classifier Accuracy: {score * 100:.2f}%")

    model_path = os.path.join(output_dir, "q_sentinel_classifier.joblib")
    joblib.dump(clf, model_path)

    # Export to ONNX
    onnx_path = os.path.join(output_dir, "q_sentinel_threat_classifier.onnx")
    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        initial_type = [('float_input', FloatTensorType([None, 11]))]
        onx = convert_sklearn(clf, initial_types=initial_type, target_opset=13)
        with open(onnx_path, "wb") as f:
            f.write(onx.SerializeToString())
        print(f"[Edge AI Train] Exported 11-feature ONNX MLP model to: {onnx_path} (Size: {os.path.getsize(onnx_path)} bytes)")
    except Exception as e:
        print(f"[Edge AI Train] ONNX conversion issue ({e}). Joblib model saved to {model_path}.")

    return onnx_path


if __name__ == "__main__":
    train_and_export_model()

