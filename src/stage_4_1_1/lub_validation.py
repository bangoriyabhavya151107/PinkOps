"""
PinkOps — Stage 4.1.1: Comprehensive LUB Simulation Truth Validation
Module: src/stage_4_1_1/lub_validation.py

Purpose:
- Rigorously validate the Lower Uncertainty Bound (LUB) against known simulation truth.
- True latent parameter: mu_i ~ N(0, tau^2 = sigma^2 / K) where K = 100, sigma = 1.10 -> tau = 0.11
- Heteroscedastic noise: sigma_i drawn uniformly from [0.70, 1.50]
- Sample size grid: n in [5, 10, 20, 50, 100, 250, 500]
- Monte Carlo trials: 2,000 synthetic players per sample size = 14,000 total synthetic players
- Evaluate:
    * empirical coverage of LUB20 (nominal: 80%)
    * coverage error
    * bias
    * empirical RMSE vs theoretical SE
    * mean interval width
    * coverage by sample size, noise level, and true parameter magnitude
- Exports: data/processed/stage_4_1_1_lub_coverage.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path


def run_comprehensive_lub_simulation(output_dir: Path, seed: int = 42):
    np.random.seed(seed)
    
    k_shrink = 100.0
    sigma_pop = 1.10
    tau_prior = sigma_pop / np.sqrt(k_shrink)  # 0.110
    
    sample_sizes = [5, 10, 20, 50, 100, 250, 500]
    n_players_per_n = 2000
    
    records = []
    player_records = []
    
    print(f"Executing LUB simulation truth validation across {len(sample_sizes)} sample size cohorts ({n_players_per_n} players each)...")
    
    for n in sample_sizes:
        # 1. Generate true latent talent parameter mu_i from prior
        true_mu = np.random.normal(loc=0.0, scale=tau_prior, size=n_players_per_n)
        
        # 2. Generate heteroscedastic within-player delivery noise
        true_sigma = np.random.uniform(low=0.70, high=1.50, size=n_players_per_n)
        
        # 3. Simulate delivery outcomes and sample mean
        # sample mean y_bar ~ N(true_mu, true_sigma^2 / n)
        y_bar = np.random.normal(loc=true_mu, scale=true_sigma / np.sqrt(n))
        
        # 4. Compute estimator under operational specification
        lambda_w = n / (n + k_shrink)
        eb_mean = lambda_w * y_bar
        se_eb = np.sqrt((sigma_pop**2) / (n + k_shrink))
        
        # 5. Compute LUBs
        lub_10 = eb_mean - 1.282 * se_eb
        lub_20 = eb_mean - 0.842 * se_eb
        lub_30 = eb_mean - 0.524 * se_eb
        
        # 6. Evaluate empirical coverage against known true_mu
        covered_10 = true_mu >= lub_10
        covered_20 = true_mu >= lub_20
        covered_30 = true_mu >= lub_30
        
        # 7. Error metrics
        errors = eb_mean - true_mu
        bias = np.mean(errors)
        rmse = np.sqrt(np.mean(errors**2))
        mean_se = np.mean(se_eb)
        
        cov_10_rate = np.mean(covered_10)
        cov_20_rate = np.mean(covered_20)
        cov_30_rate = np.mean(covered_30)
        
        int_width_90 = 2.0 * 1.645 * se_eb
        
        records.append({
            "sample_size_n": n,
            "n_synthetic_players": n_players_per_n,
            "nominal_coverage_lub20": 0.8000,
            "empirical_coverage_lub20": round(float(cov_20_rate), 4),
            "coverage_error_lub20": round(float(cov_20_rate - 0.8000), 4),
            "empirical_coverage_lub10": round(float(cov_10_rate), 4),
            "empirical_coverage_lub30": round(float(cov_30_rate), 4),
            "mean_bias": round(float(bias), 5),
            "empirical_rmse": round(float(rmse), 4),
            "theoretical_se": round(float(mean_se), 4),
            "rmse_ratio": round(float(rmse / mean_se), 4),
            "mean_uncertainty_width_90": round(float(np.mean(int_width_90)), 4)
        })
        
        # Collect for parameter magnitude breakdown
        for i in range(n_players_per_n):
            player_records.append({
                "n": n,
                "true_mu": true_mu[i],
                "true_sigma": true_sigma[i],
                "abs_mu": np.abs(true_mu[i]),
                "covered_20": int(covered_20[i])
            })
            
    df_results = pd.DataFrame(records)
    
    # Save primary coverage table
    csv_path = output_dir / "stage_4_1_1_lub_coverage.csv"
    df_results.to_csv(csv_path, index=False)
    print(f"Saved LUB coverage results to {csv_path}")
    print(df_results.to_string(index=False))
    
    # Analyze by parameter magnitude and noise level
    df_players = pd.DataFrame(player_records)
    print("\n--- Coverage by True Parameter Magnitude (Abs Latent Value) ---")
    df_players['mag_bin'] = pd.qcut(df_players['abs_mu'], q=4, labels=['Low (<25%)', 'Mid-Low (25-50%)', 'Mid-High (50-75%)', 'High (>75%)'])
    print(df_players.groupby('mag_bin', observed=False)['covered_20'].mean())
    
    print("\n--- Coverage by Within-Player Noise (Sigma) ---")
    df_players['sigma_bin'] = pd.cut(df_players['true_sigma'], bins=[0.7, 0.9, 1.1, 1.3, 1.5], labels=['0.7-0.9', '0.9-1.1', '1.1-1.3', '1.3-1.5'])
    print(df_players.groupby('sigma_bin', observed=False)['covered_20'].mean())
    
    return df_results, df_players


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    out_dir = proj_root / "data" / "processed"
    run_comprehensive_lub_simulation(out_dir)
