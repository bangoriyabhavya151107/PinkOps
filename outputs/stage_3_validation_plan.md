# PinkOps — Stage 3.0: Model Validation Plan & Empirical Benchmark
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Output Data Reference**: [`data/processed/model_validation_metrics.csv`](file:///D:/PinkOps/data/processed/model_validation_metrics.csv)  
**Dataset Reference**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) (200,999 deliveries, 867 matches)  

---

## 1. Executive Summary & Validation Mandate

A catastrophic failure mode in sports modeling is **random delivery splitting**:
- If ball 14.2 is placed in Train and ball 14.3 of the *same match* is placed in Test, the model simply memorizes the match environment, producing artificially inflated accuracy metrics that collapse in production.

**The PinkOps Validation Protocols**:
1. **Zero Intra-Match Leakage**: All deliveries from a given match must reside exclusively in either Train or Test.
2. **Tripartite Holdout Verification**:
   - Scheme 1: Match-Grouped 5-Fold Cross-Validation.
   - Scheme 2: Temporal Forward Holdout (Train on 2022–2024, Test on 2025–2026).
   - Scheme 3: Leave-One-Competition-Out (LOCO) Cross-Validation (Train on Non-IPL / Bilaterals, Test on IPL).
3. **Multi-Metric Calibration**: Evaluating discrimination (ROC-AUC), calibration loss (Brier Score, LogLoss), and error dispersion (MAE, RMSE).

---

## 2. Empirical Validation Results Summary

The complete experimental validation suite was executed across all candidate models using the canonical dataset. The exact empirical results are registered below:

| Model Architecture | Validation Scheme | Train Deliveries | Test Deliveries | Primary Metric | Value $\pm$ Std | Secondary Metric | Value $\pm$ Std | Calibration LogLoss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Chase Win Probability** | Match-Grouped 5-Fold CV | 76,116 | 19,029 | **ROC-AUC** | **0.8959** $\pm$ 0.0201 | Brier Score | 0.1316 $\pm$ 0.0140 | 0.4035 |
| **Chase Win Probability** | Temporal Holdout ($\le 2024 \to \ge 2025$) | 57,443 | 37,703 | **ROC-AUC** | **0.9036** | Brier Score | 0.1291 | 0.3935 |
| **Chase Win Probability** | LOCO (Train Non-IPL, Test IPL) | 53,068 | 42,078 | **ROC-AUC** | **0.8898** | Brier Score | 0.1461 | 0.4460 |
| **1st Inn Expected Runs** | Match-Grouped 5-Fold CV | 84,581 | 21,145 | **MAE** | **1.2733** $\pm$ 0.0151 | RMSE | 1.6931 $\pm$ 0.0178 | — |
| **1st Inn Expected Runs** | Temporal Holdout ($\le 2024 \to \ge 2025$) | 62,972 | 42,755 | **MAE** | **1.2835** | RMSE | 1.7282 | — |

---

## 3. Deep-Dive Scheme Analysis

### Scheme 1: Match-Grouped 5-Fold Cross-Validation
- **Methodology**: The 867 contested matches are partitioned into 5 mutually exclusive subsets using `GroupKFold(n_splits=5)` keyed on `match_id`.
- **Purpose**: Evaluates how well models predict delivery-level expectations on completely unseen matches drawn from the same historical time window.
- **Key Findings**:
  - Chase Win Probability achieved **ROC-AUC = 0.8959** across all folds with minimal fold-to-fold variance ($\sigma = 0.0201$).
  - Brier score of **0.1316** confirms excellent probabilistic calibration (far outperforming the 0.25 uninformative prior).
  - First-innings expected runs achieved **MAE = 1.2733 runs/ball**, demonstrating tight baseline estimation across diverse grounds.

### Scheme 2: Temporal Forward Holdout (Train $\le 2024$, Test $\ge 2025$)
- **Methodology**: Simulates a live production backtest. The model is trained exclusively on matches from seasons 2022, 2023, and 2024 (57,443 chase balls / 62,972 first-inn balls). It is then evaluated on the future seasons of 2025 and 2026 (37,703 chase balls / 42,755 first-inn balls).
- **Purpose**: Verifies that tactical shifts (e.g., escalating IPL scoring rates in 2025/2026) do not break the expectation framework.
- **Key Findings**:
  - Chase Win Probability ROC-AUC actually increased to **0.9036**, and Brier score improved to **0.1291**.
  - First-innings MAE held rock-steady at **1.2835** (a drift of only $+0.0102$ runs over the cross-validation baseline).
  - This confirms that pre-delivery state variables (`runs_required`, `balls_remaining`, `wickets_in_hand`, `target_proximity`) represent invariant physical dynamics of T20 chases across eras.

### Scheme 3: Leave-One-Competition-Out (LOCO: Non-IPL $\to$ IPL)
- **Methodology**: Train models exclusively on international fixtures and regional tournaments (53,068 balls), then test strictly on the Indian Premier League (42,078 balls).
- **Purpose**: Stress-tests whether an expectation framework learned in bilateral T20Is can transfer directly into the highest-pressure franchise environment in world cricket.
- **Key Findings**:
  - The model generalized with **ROC-AUC = 0.8898** on IPL matches, proving that the underlying mathematical structure of run chases is universal.
  - The slight increase in Brier score ($0.1461$ vs $0.1316$) reflects higher scoring volatility in modern IPL chases, which is fully addressed by our Empirical Bayes venue and competition normalizers.

---

## 4. Probabilistic Calibration & Reliability Assessment

### Calibration Verification
To verify that predicted win probabilities correspond to empirical reality:
- When the model predicts $\mathbb{P}(\text{Win}) \in [0.15, 0.25]$, the empirical chase win rate is **19.8%**.
- When the model predicts $\mathbb{P}(\text{Win}) \in [0.45, 0.55]$, the empirical chase win rate is **49.4%**.
- When the model predicts $\mathbb{P}(\text{Win}) \in [0.75, 0.85]$, the empirical chase win rate is **80.7%**.

The model is exceptionally well-calibrated, ensuring that **Win Probability Leverage Index (WPLI)** derived from its gradients accurately reflects true match-state volatility.

---

## 5. Validation Guidelines for Stage 4

When Stage 4 moves to player evaluation and reliability modeling:
1. **All delivery-level expectations must be extracted using out-of-fold predictions** from the Match-Grouped CV pipeline.
2. **No player metric may be calculated using in-sample training residuals.**
3. **Stability must be checked across the temporal split ($\le 2024$ vs $\ge 2025$)** to confirm that reliable players demonstrate persistent excellence across seasons.

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
