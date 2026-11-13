"""
PinkOps — Stage 4.0: Uncertainty & Empirical Bayes Shrinkage Module (Remediated)
Module: src/stage_4_0/uncertainty.py

Purpose:
- Estimate conservative performance bounds via Empirical Bayes shrinkage.
- Compute Lower Uncertainty Bounds (LUB 10th, 20th, 25th, 30th percentiles).
- Explicitly retain raw estimates, shrunk estimates, and uncertainty bounds.
- Normal-approximation lower uncertainty bound (LUB / conservative lower bound).
"""

import pandas as pd
import numpy as np


def estimate_uncertainty(
    player_df: pd.DataFrame, 
    value_col: str = 'raw_va_per_ball',
    sample_col: str = 'total_deliveries',
    k_shrink: float = 100.0,
    sigma: float = 1.10
) -> pd.DataFrame:
    """
    Computes Empirical Bayes shrinkage and multiple Lower Uncertainty Bound (LUB) percentiles.
    
    Parameters:
    - player_df: DataFrame with player-level summary
    - value_col: column containing observed mean rate
    - sample_col: column containing sample size (ball count)
    - k_shrink: shrinkage prior strength (pseudo-observations, primary: 100.0)
    - sigma: population standard deviation of delivery-level outcomes (default: 1.10)
    
    Returns:
    - DataFrame enriched with EB-shrunk estimate, standard error, uncertainty width, and LUB percentiles.
    """
    df = player_df.copy()
    n = df[sample_col].astype(float)
    x = df[value_col].astype(float)
    pop_mean = 0.0  # Population expectation baseline has zero mean value added
    
    # Shrinkage weight lambda in [0, 1]
    lambda_weight = n / (n + k_shrink)
    
    # Empirical Bayes shrunk estimate
    eb_shrunk_estimate = lambda_weight * x + (1.0 - lambda_weight) * pop_mean
    
    # Standard error of estimator combining within-player variance and prior variance
    se_eb = np.sqrt((sigma**2) / (n + k_shrink) + (k_shrink * (sigma**2)) / ((n + k_shrink)**2))
    
    # Uncertainty interval width (90% two-sided width)
    uncertainty_width_90 = 2.0 * 1.645 * se_eb
    
    # Lower Uncertainty Bound (LUB) variants
    # LUB 20th percentile:
    # "provisional conservative decision metric supported by sensitivity stability"
    lub_10 = eb_shrunk_estimate - 1.282 * se_eb
    lub_20 = eb_shrunk_estimate - 0.842 * se_eb
    lub_25 = eb_shrunk_estimate - 0.674 * se_eb
    lub_30 = eb_shrunk_estimate - 0.524 * se_eb
    
    df['shrinkage_weight'] = round(lambda_weight, 4)
    df['eb_shrunk_estimate'] = round(eb_shrunk_estimate, 4)
    df['se_eb'] = round(se_eb, 4)
    df['uncertainty_width_90'] = round(uncertainty_width_90, 4)
    
    # Primary Lower Uncertainty Bounds
    df['lub_10'] = round(lub_10, 4)
    df['lub_20'] = round(lub_20, 4)
    df['lub_25'] = round(lub_25, 4)
    df['lub_30'] = round(lub_30, 4)
    
    # Backwards-compatible aliases for LCB naming convention
    df['lcb_10'] = df['lub_10']
    df['lcb_20'] = df['lub_20']
    df['lcb_25'] = df['lub_25']
    df['lcb_30'] = df['lub_30']
    df['posterior_mean'] = df['eb_shrunk_estimate']
    df['posterior_se'] = df['se_eb']
    
    return df
