"""
Evaluation Metrics & Performance Analysis for QDS Security Detector.

Computes:
- True Positive Rate (TPR)
- False Positive Rate (FPR)
- False Accept Rate (FAR)
- False Reject Rate (FRR)
- Overall Accuracy
- Latency & Shot Efficiency
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EvaluationMetrics:
    """Security performance summary metrics."""
    total_experiments: int = 0
    clean_runs: int = 0
    attack_runs: int = 0
    
    true_positives: int = 0   # Attack correctly flagged REJECT / SUSPICIOUS
    true_negatives: int = 0   # Clean correctly passed ACCEPT
    false_positives: int = 0  # Clean incorrectly rejected / flagged SUSPICIOUS (False Reject)
    false_negatives: int = 0  # Attack incorrectly passed ACCEPT (False Accept)
    
    @property
    def tpr(self) -> float:
        """True Positive Rate (Sensitivity / Recall)."""
        denom = self.true_positives + self.false_negatives
        return float(self.true_positives / denom) if denom > 0 else 0.0

    @property
    def fpr(self) -> float:
        """False Positive Rate."""
        denom = self.false_positives + self.true_negatives
        return float(self.false_positives / denom) if denom > 0 else 0.0

    @property
    def far(self) -> float:
        """False Accept Rate (Critical Security Metric)."""
        return float(self.false_negatives / self.attack_runs) if self.attack_runs > 0 else 0.0

    @property
    def frr(self) -> float:
        """False Reject Rate (Usability Metric)."""
        return float(self.false_positives / self.clean_runs) if self.clean_runs > 0 else 0.0

    @property
    def accuracy(self) -> float:
        """Overall detection accuracy."""
        total = self.total_experiments
        correct = self.true_positives + self.true_negatives
        return float(correct / total) if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_experiments": self.total_experiments,
            "clean_runs": self.clean_runs,
            "attack_runs": self.attack_runs,
            "true_positives": self.true_positives,
            "true_negatives": self.true_negatives,
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "tpr": self.tpr,
            "fpr": self.fpr,
            "far": self.far,
            "frr": self.frr,
            "accuracy": self.accuracy,
        }


def compute_batch_metrics(results: List[Dict[str, Any]]) -> EvaluationMetrics:
    """Compute summary security metrics over a dataset of experiment results."""
    eval_m = EvaluationMetrics()
    eval_m.total_experiments = len(results)
    
    for r in results:
        is_attack = (r.get("attack_type", "none") != "none") or (r.get("attack_severity", 0.0) > 0.0)
        decision = r.get("decision", "ACCEPT")
        
        if is_attack:
            eval_m.attack_runs += 1
            if decision in ["REJECT", "SUSPICIOUS"]:
                eval_m.true_positives += 1
            else:
                eval_m.false_negatives += 1  # False Accept
        else:
            eval_m.clean_runs += 1
            if decision == "ACCEPT":
                eval_m.true_negatives += 1
            else:
                eval_m.false_positives += 1  # False Reject
                
    return eval_m
