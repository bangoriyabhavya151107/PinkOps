# PinkOps — Stage 4.0: Reliability Validation Plan & Statistical Verification Protocols

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_validation_plan.md`  
**Stage:** 4.0 — Reliability Architecture, Estimand Freeze & Governance  
**Governance Status:** FROZEN VALIDATION PLAN (Pre-Registration Before Player Selection)  

---

## 1. Executive Summary & Purpose

A fundamental mandate of quantitative sports science is **pre-registration of validation protocols**. Testing model validity only after seeing player rankings allows researchers to alter validation schemes until favored players look good.

This document formally establishes the five-pillar validation plan for the **Seven-Layer Reliability Architecture**. These statistical protocols verify that our expectation baselines, pressure indices, value-added metrics, and uncertainty bounds are calibrated, generalizable across leagues, and temporally stable, with strict stopping criteria defined in advance.

---

## 2. The Five Pillars of Architectural Validation

```
                                      [ FIVE PILLARS OF VALIDATION ]
                                                    │
             ┌──────────────────────────────┬───────┴───────┬──────────────────────────────┐
             ▼                              ▼               ▼                              ▼
      [ PILLAR 1 ]                   [ PILLAR 2 ]    [ PILLAR 3 ]                   [ PILLAR 4 ]
    Match-Grouped K-Fold         Temporal Forward     Leave-One-Comp              Calibration &
      Cross-Validation              Chaining          Out (LOCO)                  Brier Analysis
    (Within-Match Isolation)     (Simulated Auction) (Cross-League)               (Reliability)
                                                            │
                                                            ▼
                                                     [ PILLAR 5 ]
                                                 Uncertainty Interval
                                                  Empirical Coverage
```

---

## 3. Detailed Specification of Validation Protocols

### 3.1 Pillar 1: Match-Grouped K-Fold Cross-Validation

#### 3.1.1 Purpose & Rationale
In delivery-level cricket data, balls within the same match share unobserved pitch wear, dew, atmospheric humidity, and umpire interpretations. Random ball-level splitting creates severe target leakage by placing balls from the same over into both train and test sets.

#### 3.1.2 Protocol
- Group 200,961 deliveries by `match_id` across 5 folds ($K = 5$).
- Ensure all deliveries from a given match exist exclusively in either the training set or the test set.
- Fit expectation models on 4 folds ($80\%$ of matches) and evaluate out-of-sample predictions on the held-out fold ($20\%$).
- Compute out-of-sample MAE, RMSE, and Log-Loss across folds.

---

### 3.2 Pillar 2: Temporal Forward-Chaining Validation

#### 3.2.1 Purpose & Rationale
In real-world franchise deployment, Rajasthan Royals must evaluate players using historical data to predict future performance in an upcoming tournament. Standard cross-validation allows past events to be predicted by future data.

#### 3.2.2 Protocol
- Partition matches chronologically by match date.
- **Split 1 (Early Career Baseline):** Train on $T_0$ to $T_1$; validate on $T_1$ to $T_2$.
- **Split 2 (Mid Horizon):** Train on $T_0$ to $T_2$; validate on $T_2$ to $T_3$.
- **Split 3 (Auction Deployment Test):** Train on all data prior to the final competitive season; evaluate out-of-time player Value Added rank correlation in the held-out season.

---

### 3.3 Pillar 3: Leave-One-Competition-Out (LOCO) Cross-Validation

#### 3.3.1 Purpose & Rationale
Players in the competition dataset compete across international tournaments, domestic leagues, and franchise competitions. An expectation model that overfits to the scoring patterns of a single tournament will misestimate player value in others.

#### 3.3.2 Protocol
- Iteratively hold out each unique competition in `data/raw/competitions.csv`.
- Train expectation baselines and venue models on the remaining $C - 1$ competitions.
- Evaluate transfer generalizability on the held-out competition using out-of-league competition baseline shrinkage.
- Metric: Prediction error degradation ratio $\frac{\text{MAE}_{\text{held-out}}}{\text{MAE}_{\text{in-sample}}}$ must remain $\le 1.08$.

---

### 3.4 Pillar 4: Probability Calibration & Brier Score Analysis

#### 3.4.1 Purpose & Rationale
The delivery expectation model generates discrete event probabilities: $\hat{P}(\text{Boundary})$, $\hat{P}(\text{Dot})$, $\hat{P}(\text{Wicket})$. If the model predicts $\hat{P}(\text{Boundary}) = 0.25$, exactly $25\%$ of those deliveries in reality must result in a boundary. Uncalibrated probabilities distort Value Added attribution.

#### 3.4.2 Protocol
- Partition predicted event probabilities into 10 deciles ($[0.0, 0.1), [0.1, 0.2), \dots, [0.9, 1.0]$).
- Plot empirical event frequency against predicted mean probability (Reliability Diagram).
- Fit logistic calibration curve: $\text{logit}(Y) = \alpha + \beta \cdot \text{logit}(\hat{P})$.
- Compute Brier Score: $\text{BS} = \frac{1}{N} \sum_{t=1}^N (Y_t - \hat{P}_t)^2$.
- Target Criteria: Slope $\beta \in [0.92, 1.08]$, Intercept $|\alpha| \le 0.05$, Brier Score improvement over naive frequency prior $\ge 8.5\%$.

---

### 3.5 Pillar 5: Empirical Bayes Uncertainty Interval Coverage

#### 3.5.1 Purpose & Rationale
Layer 5 produces Empirical Bayes credible intervals ($\text{LCB}_{10}, \text{LCB}_{20}, \text{LCB}_{25}, \text{LCB}_{30}$). For these bounds to be mathematically honest, a nominal $80\%$ one-sided lower credible bound ($\text{LCB}_{20}$) must bound the true latent mean from below in at least $80\%$ of bootstrap replications.

#### 3.5.2 Protocol
- Perform match-clustered bootstrap resampling ($B = 1,000$ iterations).
- For each player with $N \ge 100$ balls, compute empirical distribution of Value Added.
- Verify whether the frozen formula $\text{LCB}_{20} = \hat{\theta}^{\text{EB}} - 0.842 \cdot \text{SE}^{\text{EB}}$ achieves empirical coverage $\ge 78.5\%$.
- Guard against under-coverage in sparse samples ($N < 50$).

---

## 4. Benchmark Standards & Formal Rejection Criteria

To maintain scientific integrity, the Quantitative Governance Committee pre-registers explicit **Model Rejection Thresholds**. If any expectation model violates these thresholds during validation, it is rejected and cannot proceed to player evaluation:

| Metric | Benchmark Target | Formal Rejection Threshold | Governance Action Upon Failure |
|---|---|---|---|
| **Delivery Run MAE (Out-of-Sample)** | $\le 0.820$ runs/ball | $> 0.860$ runs/ball | Re-tune feature representations |
| **Delivery Run RMSE (Out-of-Sample)** | $\le 1.350$ runs/ball | $> 1.450$ runs/ball | Check outlier loss clipping |
| **Boundary Brier Score Improvement** | $\ge 8.0\%$ vs. Prior | $< 4.0\%$ vs. Prior | Reject probability estimator |
| **Wicket Brier Score Improvement** | $\ge 3.0\%$ vs. Prior | $< 1.0\%$ vs. Prior | Re-weight class imbalance |
| **Calibration Curve Slope $\beta$** | $1.00 \pm 0.05$ | $\beta < 0.85 \lor \beta > 1.18$ | Apply isotonic or Platt calibration |
| **LOCO Generalization Ratio** | $\le 1.05$ | $> 1.15$ | Increase competition shrinkage |
| **LCB20 Empirical Coverage** | $\ge 80.0\%$ | $< 75.0\%$ | Expand standard error formula |
| **Temporal Forward Rank Correlation** | $r_s \ge 0.65$ | $r_s < 0.45$ | Reject model for auction use |

---

## 5. Summary & Governance Sign-Off

The five-pillar validation plan establishes unambiguous statistical criteria for verifying Operation Pink Panther. No model will be accepted for player selection in Stage 4.1 unless it satisfies every benchmark specified in this pre-registered protocol.

*Document Approved by PinkOps Quantitative Governance Committee.*
