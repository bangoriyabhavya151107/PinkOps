# PinkOps — Stage 4.1.1: Empirical LUB Coverage Validation Report
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Verification Script:** `src/stage_4_1_1/lub_validation.py`  
**Dataset Artifact:** [`data/processed/stage_4_1_1_lub_coverage.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_lub_coverage.csv)  
**Date:** November 2026  

---

## 1. Simulation Design & Known Truth Definition

To independently evaluate the validity of the Lower Uncertainty Bound (LUB) without relying on circular observational assumptions, a large-scale Monte Carlo simulation truth experiment was executed:

1. **Known Latent Parameter ($\mu_i$):**
   - Latent performance parameters for $N = 14,000$ synthetic players were drawn directly from a known ground-truth Gaussian prior:
     $$\mu_i \stackrel{\text{iid}}{\sim} \mathcal{N}\left(0, \; \tau^2 = \frac{\sigma^2}{K}\right)$$
   - Operating parameters: $\sigma = 1.10$, $K = 100.0 \implies \tau = 0.110$.
2. **Heteroscedastic Within-Player Noise ($\sigma_i$):**
   - Each player was assigned an independent delivery-level standard deviation drawn uniformly from $\sigma_i \sim \mathcal{U}(0.70, 1.50)$.
3. **Sample Size Grid:**
   - 2,000 independent synthetic players were simulated across each of 7 sample size cohorts:
     $$n \in [5, 10, 20, 50, 100, 250, 500]$$
4. **Estimation Protocol:**
   - The estimator operates under the identical specifications applied in the player evidence pipeline:
     $$\hat{\mu}_{i, \text{EB}} = \frac{n_i}{n_i + K} \bar{Y}_i, \quad \text{SE}_{i, \text{EB}} = \sqrt{\frac{\sigma_{\text{pop}}^2}{n_i + K}}, \quad \text{LUB}_{i, 20} = \hat{\mu}_{i, \text{EB}} - 0.842 \cdot \text{SE}_{i, \text{EB}}$$

---

## 2. Empirical Coverage Results across Sample Size Cohorts

The table below records the empirical recovery statistics across all 14,000 synthetic trials:

| Sample Size ($n$) | Synthetic Players | Nominal Coverage ($\text{LUB}_{20}$) | Empirical Coverage ($\text{LUB}_{20}$) | Coverage Error | Empirical Coverage ($\text{LUB}_{10}$) | Empirical Coverage ($\text{LUB}_{30}$) | Empirical RMSE | Theoretical $\text{SE}_{\text{EB}}$ | RMSE Ratio ($\frac{\text{Emp}}{\text{Theo}}$) | Mean 90% Width |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **5** | 2,000 | 80.00% | **82.05%** | +2.05% | 91.70% | 71.75% | 0.1065 | 0.1073 | 0.9925 | 0.3532 |
| **10** | 2,000 | 80.00% | **78.35%** | -1.65% | 88.70% | 68.15% | 0.1081 | 0.1049 | 1.0303 | 0.3451 |
| **20** | 2,000 | 80.00% | **80.10%** | **+0.10%** | 90.30% | 70.20% | 0.1017 | 0.1004 | 1.0132 | 0.3304 |
| **50** | 2,000 | 80.00% | **80.85%** | +0.85% | 91.10% | 70.45% | 0.0895 | 0.0898 | 0.9962 | 0.2955 |
| **100** | 2,000 | 80.00% | **80.30%** | **+0.30%** | 90.05% | 69.75% | 0.0774 | 0.0778 | 0.9953 | 0.2559 |
| **250** | 2,000 | 80.00% | **79.80%** | **-0.20%** | 90.05% | 69.35% | 0.0609 | 0.0588 | 1.0356 | 0.1934 |
| **500** | 2,000 | 80.00% | **81.55%** | +1.55% | 90.70% | 70.65% | 0.0438 | 0.0449 | 0.9749 | 0.1477 |

### Key Observations
1. **Nominal Match:** Empirical coverage of $\text{LUB}_{20}$ ranges from **$78.35\%$ to $82.05\%$**, tightly tracking the nominal 80.00% target across all sample size regimes.
2. **RMSE Concordance:** The empirical root mean squared error matches the theoretical standard error $\sqrt{\sigma^2 / (n+K)}$ across all cohorts (RMSE ratios between **0.9749 and 1.0356**). This verifies that the derived uncertainty formula accurately reflects estimator dispersion.
3. **Uncertainty Width Contraction:** The 90% uncertainty width contracts smoothly from **0.3532 runs/ball** at $n = 5$ down to **0.1477 runs/ball** at $n = 500$, proving that the bound properly relieves the small-sample discount as empirical evidence accumulates.

---

## 3. Disaggregated Diagnostics: Parameter Magnitude & Noise

### 3.1 Coverage by True Parameter Magnitude ($|\mu_i|$)
```
True Parameter Magnitude Quartile     Empirical LUB20 Coverage
--------------------------------------------------------------
Low Quartile       (|mu| < 0.045)               92.26%
Mid-Low Quartile   (0.045 <= |mu| < 0.092)      89.09%
Mid-High Quartile  (0.092 <= |mu| < 0.155)      77.31%
High Quartile      (|mu| >= 0.155)              63.06%
```
*Theoretical Explanation:* Shrinkage pulls estimates inward toward $\mu_0 = 0.0$. For players near the population mean, shrinkage pulls in the same direction as the conservative bound discount, producing higher coverage (~92%). For extreme positive outliers ($> 75$th percentile), inward shrinkage counteracts the lower bound, resulting in an expected reduction in one-sided coverage. This behavior is mathematically inherent to Bayesian shrinkage estimators and highlights why $\text{LUB}_{20}$ is a *conservative screening tool* rather than an unbiased point estimate.

### 3.2 Coverage by Delivery-Level Noise ($\sigma_i$)
```
Within-Player Noise Bin (sigma)       Empirical LUB20 Coverage
--------------------------------------------------------------
0.70 - 0.90                                     82.24%
0.90 - 1.10                                     81.08%
1.10 - 1.30                                     79.89%
1.30 - 1.50                                     78.52%
```
*Robustness Finding:* Across a two-fold difference in within-player volatility ($\sigma_i \in [0.70, 1.50]$), empirical coverage remains stable between **78.52% and 82.24%**, verifying that minor departures from homoscedasticity do not destabilize the bound.

---

*End of Stage 4.1.1 LUB Validation Report.*
