"""
Statistical Evaluation Engine for QDS Threat Detector.

Pure rule-based statistical hypothesis testing with NO AI/ML:
- Empirical outcome probabilities p_hat = k / N
- Binomial Standard Error SE = sqrt(p0 * (1 - p0) / N)
- Z-score calculation z = (p_hat - p0) / SE
- Chi-square goodness-of-fit test and p-value derivation
- Maximum probability deviation max |p_hat_i - p0_i|
- Confidence interval bounds (Agresti-Coull / Wilson score)
"""

from typing import Dict, Any, Tuple
import numpy as np
from scipy import stats


def compute_probability_deviation(
    observed_probs: Dict[str, float],
    baseline_probs: Dict[str, float]
) -> float:
    """Compute maximum absolute probability deviation max |p_hat_i - p0_i|."""
    max_dev = 0.0
    for outcome in ["+1", "-1"]:
        p_obs = observed_probs.get(outcome, 0.0)
        p_base = baseline_probs.get(outcome, 0.0)
        dev = abs(p_obs - p_base)
        if dev > max_dev:
            max_dev = dev
    return float(max_dev)


def compute_z_score_and_p_value(
    observed_counts: Dict[str, int],
    baseline_probs: Dict[str, float],
    shots: int
) -> Tuple[float, float, float]:
    """
    Compute z-score statistic and 2-sided p-value for primary (+1) outcome.
    Returns (z_score, p_value, standard_error).
    """
    k = observed_counts.get("+1", 0)
    p_obs = k / shots
    p0 = baseline_probs.get("+1", 0.5)
    
    # Handle boundary baseline (p0 = 1.0 or p0 = 0.0) using max of baseline and sample variance
    var_base = p0 * (1.0 - p0)
    var_sample = p_obs * (1.0 - p_obs)
    effective_var = max(var_base, var_sample, 1e-8)
    se = np.sqrt(effective_var / shots)
    
    if abs(p_obs - p0) < 1e-9:
        z_score = 0.0
        p_value = 1.0
    elif se <= 0:
        z_score = 0.0
        p_value = 1.0
    else:
        z_score = (p_obs - p0) / se
        p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z_score)))
        
    return float(z_score), float(p_value), float(se)


def compute_chi_square_test(
    observed_counts: Dict[str, int],
    baseline_probs: Dict[str, float],
    shots: int
) -> Tuple[float, float]:
    """
    Compute Chi-square goodness-of-fit statistic chi2 and p-value.
    chi2 = sum (O_i - E_i)^2 / E_i
    """
    f_obs = []
    f_exp = []
    
    for outcome in ["+1", "-1"]:
        obs = observed_counts.get(outcome, 0)
        p0 = baseline_probs.get(outcome, 0.5)
        exp = max(1e-6, p0 * shots)
        
        f_obs.append(obs)
        f_exp.append(exp)
        
    chi2, p_val = stats.chisquare(f_obs=f_obs, f_exp=f_exp)
    return float(chi2), float(p_val)


def compute_confidence_intervals(
    observed_counts: Dict[str, int],
    shots: int,
    confidence_level: float = 0.99
) -> Dict[str, Tuple[float, float]]:
    """Compute Wilson score confidence intervals for outcomes +1 and -1."""
    alpha = 1.0 - confidence_level
    z = stats.norm.ppf(1.0 - alpha / 2.0)
    
    intervals = {}
    for outcome in ["+1", "-1"]:
        k = observed_counts.get(outcome, 0)
        p_hat = k / shots
        
        # Wilson score interval formula
        denom = 1.0 + (z**2) / shots
        center = (p_hat + (z**2) / (2.0 * shots)) / denom
        delta = (z / denom) * np.sqrt((p_hat * (1.0 - p_hat) / shots) + (z**2) / (4.0 * (shots**2)))
        
        lower = max(0.0, center - delta)
        upper = min(1.0, center + delta)
        intervals[outcome] = (float(lower), float(upper))
        
    return intervals
