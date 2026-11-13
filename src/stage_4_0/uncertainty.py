"""
PinkOps — Stage 4.1.1: Uncertainty & Empirical Bayes Shrinkage Module (Hardened)
Module: src/stage_4_0/uncertainty.py

Purpose:
- Formally derive and compute Empirical Bayes shrinkage and Lower Uncertainty Bounds (LUB).
- Standard Error derived as the exact root expected MSE / conjugate posterior standard deviation:
    SE_EB = sqrt( sigma^2 / (n + K) )
- Eliminates ad-hoc variance inflation and provides mathematically rigorous frequentist bounds.
- Retains raw estimates, shrunk estimates, SE, and multi-percentile LUBs (10, 15, 20, 25, 30).
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
    Computes Empirical Bayes shrinkage and Lower Uncertainty Bounds (LUB).
    
    Mathematical Derivation:
    - Prior on latent talent: mu_i ~ N(mu_0, tau^2), with mu_0 = 0.0 (league expectation)
    - Sampling model: y_bar_i | mu_i ~ N(mu_i, sigma^2 / n_i)
    - Let K = sigma^2 / tau^2. Shrinkage weight lambda_i = n_i / (n_i + K).
    - Shrunk Estimator: mu_hat_EB = lambda_i * y_bar_i + (1 - lambda_i) * mu_0
    - Exact Expected MSE / Conjugate Posterior SD:
        SE_EB = sqrt( sigma^2 / (n_i + K) )
      At n_i -> 0: SE_EB -> tau = sigma / sqrt(K) (prior population spread)
      At n_i -> inf: SE_EB -> sigma / sqrt(n_i) (classical sampling error)
      
    - Lower Uncertainty Bound (LUB):
        LUB_alpha = mu_hat_EB - z_alpha * SE_EB
      For alpha = 0.20 (LUB20): z_0.20 = 0.842
    
    Parameters:
    - player_df: DataFrame with player-level summary
    - value_col: column containing observed mean rate
    - sample_col: column containing sample size (ball count)
    - k_shrink: shrinkage prior strength (pseudo-observations, default: 100.0)
    - sigma: population standard deviation of delivery-level outcomes (default: 1.10)
    
    Returns:
    - DataFrame enriched with shrunk estimate, SE, uncertainty width, and LUB percentiles.
    """
    df = player_df.copy()
    n = df[sample_col].astype(float)
    x = df[value_col].astype(float)
    pop_mean = 0.0  # League expectation baseline has zero mean value added
    
    # Shrinkage weight lambda in [0, 1]
    lambda_weight = n / (n + k_shrink)
    
    # Empirical Bayes shrunk estimate
    eb_shrunk_estimate = lambda_weight * x + (1.0 - lambda_weight) * pop_mean
    
    # Formally derived standard error: root expected MSE / conjugate posterior SD
    se_eb = np.sqrt((sigma**2) / (n + k_shrink))
    
    # Uncertainty interval width (90% two-sided width: z_0.05 = 1.645)
    uncertainty_width_90 = 2.0 * 1.645 * se_eb
    
    # Lower Uncertainty Bounds across pre-registered quantiles
    lub_10 = eb_shrunk_estimate - 1.282 * se_eb
    lub_15 = eb_shrunk_estimate - 1.036 * se_eb
    lub_20 = eb_shrunk_estimate - 0.842 * se_eb
    lub_25 = eb_shrunk_estimate - 0.674 * se_eb
    lub_30 = eb_shrunk_estimate - 0.524 * se_eb
    
    df['shrinkage_weight'] = round(lambda_weight, 4)
    df['eb_shrunk_estimate'] = round(eb_shrunk_estimate, 4)
    df['se_eb'] = round(se_eb, 4)
    df['uncertainty_width_90'] = round(uncertainty_width_90, 4)
    
    # Primary Lower Uncertainty Bounds
    df['lub_10'] = round(lub_10, 4)
    df['lub_15'] = round(lub_15, 4)
    df['lub_20'] = round(lub_20, 4)
    df['lub_25'] = round(lub_25, 4)
    df['lub_30'] = round(lub_30, 4)
    
    # Calibrated descriptive aliases
    df['lower_uncertainty_bound_20'] = df['lub_20']
    df['conservative_mean_estimate'] = df['eb_shrunk_estimate']
    
    return df
