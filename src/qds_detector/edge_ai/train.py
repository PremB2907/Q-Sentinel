"""
Training & ONNX Export Pipeline for Edge Threat Classifier.
SIH26141 • Egreen Quanta
Qualcomm Snapdragon AI Lab Challenge
"""

import os
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, accuracy_score
import joblib

from qds_detector.edge_ai.dataset_generator import generate_synthetic_dataset, LABEL_MAP, REVERSE_LABEL_MAP
from qds_detector.edge_ai.features import extract_batch_features, FEATURE_NAMES


def train_and_export_model(
    output_dir: str | None = None,
    num_samples: int = 1500,
    seed: int = 42
) -> str:
    """
    Trains a compact MLP threat classifier (11 -> 32 -> 16 -> 3) on synthetic telemetry,
    computes full precision/recall/F1/confusion matrix, tests on held-out dataset,
    and exports ONNX model.
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n=================================================================")
    print(f"[Edge AI Train] Starting Training Pipeline (Seed={seed}, Samples={num_samples})")
    print(f"[Edge AI Train] Feature Vector (Len={len(FEATURE_NAMES)}): {FEATURE_NAMES}")
    print(f"=================================================================")

    # 1. Primary Dataset Generation & Split
    events, labels = generate_synthetic_dataset(num_samples=num_samples, seed=seed)
    X = extract_batch_features(events)
    y = np.array(labels, dtype=int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)

    print(f"[Edge AI Train] Train set shape: {X_train.shape}, Test set shape: {X_test.shape}")
    train_dist = {REVERSE_LABEL_MAP[k]: int(v) for k, v in zip(*np.unique(y_train, return_counts=True))}
    test_dist = {REVERSE_LABEL_MAP[k]: int(v) for k, v in zip(*np.unique(y_test, return_counts=True))}
    print(f"[Edge AI Train] Train Class Distribution: {train_dist}")
    print(f"[Edge AI Train] Test Class Distribution:  {test_dist}")

    # 2. Train exact compact MLP: 11 -> 32 (ReLU) -> 16 (ReLU) -> 3 (Softmax)
    clf = MLPClassifier(
        hidden_layer_sizes=(32, 16),
        activation="relu",
        solver="adam",
        learning_rate_init=0.005,
        max_iter=1000,
        random_state=seed
    )
    clf.fit(X_train, y_train)

    # 3. Test Set Evaluation
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n[Primary Test Set Evaluation]")
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall:    {rec * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")
    print(f"\nConfusion Matrix:\n{cm}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['NORMAL', 'SUSPICIOUS', 'ATTACK'])}")

    # 4. Held-out Independent Test Set Evaluation (Seed = 100)
    print(f"[Edge AI Train] Generating Independent Held-Out Evaluation Set (Seed=100, Samples=1500)...")
    held_events, held_labels = generate_synthetic_dataset(num_samples=1500, seed=100)
    X_held = extract_batch_features(held_events)
    y_held = np.array(held_labels, dtype=int)
    
    y_held_pred = clf.predict(X_held)
    held_acc = accuracy_score(y_held, y_held_pred)
    held_prec, held_rec, held_f1, _ = precision_recall_fscore_support(y_held, y_held_pred, average="weighted")
    print(f"\n[Independent Held-Out Evaluation (Seed=100)]")
    print(f"Accuracy:  {held_acc * 100:.2f}%")
    print(f"Precision: {held_prec * 100:.2f}%")
    print(f"Recall:    {held_rec * 100:.2f}%")
    print(f"F1 Score:  {held_f1 * 100:.2f}%")

    model_path = os.path.join(output_dir, "q_sentinel_classifier.joblib")
    joblib.dump(clf, model_path)

    # 5. Export to ONNX
    onnx_path = os.path.join(output_dir, "q_sentinel_threat_classifier.onnx")
    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        initial_type = [('float_input', FloatTensorType([None, 11]))]
        onx = convert_sklearn(clf, initial_types=initial_type, target_opset=13)
        with open(onnx_path, "wb") as f:
            f.write(onx.SerializeToString())
        file_size = os.path.getsize(onnx_path)
        print(f"\n[Edge AI Train] Exported 11-feature ONNX MLP model to: {onnx_path} (Size: {file_size} bytes)")
    except Exception as e:
        print(f"\n[Edge AI Train] ONNX conversion issue ({e}). Joblib model saved to {model_path}.")

    return onnx_path


if __name__ == "__main__":
    train_and_export_model()


