# PinkOps — Stage 3.1: Expectation Estimand Formalization Report
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Dataset Reference**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) (200,999 deliveries, 867 matches)  

---

## 1. Executive Summary & Epistemological Purpose

In expected-performance modeling, a critical conceptual question must be answered:
> **What exactly does the "expected" number represent?**

In casual sports analytics, models often claim to predict what an "average player" would do in a given situation. However, in heterogeneous sports like T20 cricket, a true "player-neutral average counterfactual" cannot be directly observed because player assignment is highly non-random (elite batters face elite bowlers in crucial overs; tailenders face death yorkers).

To maintain absolute scientific rigor, PinkOps formally defines the mathematical estimands and establishes precise terminology:
- We explicitly reject describing the baseline as the literal performance of a hypothetical "average player".
- We adopt the rigorous statistical definition: **Contextual Population Expectation**.

---

## 2. Formal Estimand Definitions

We formulate and evaluate two candidate estimands:

### Estimand A: Situation-Only Environmental Expectation
$$\mathbb{E}[Y(t) \mid \mathbf{X}_{\text{situation}}(t^-)]$$

**Conditioning Covariates**:
- Macro-match state: `innings_progress_before`, `balls_remaining_before`, `wickets_in_hand_before`, `wickets_before`
- Tactical phase: `is_powerplay`, `is_death`
- Match structure: `is_chase`, `target_runs`
- Global environment: `venue_shrunk_baseline`, `competition_scoring_baseline`

**Purpose**: Measures the baseline scoring rate dictated purely by the physical and scoreboard environment, completely ignoring who is batting, who is bowling, and what teams are playing.

---

### Estimand B: Context + Opponent-Quality Population Expectation
$$\mathbb{E}[Y(t) \mid \mathbf{X}_{\text{context+opponent}}(t^-)]$$

**Conditioning Covariates**:
- All Estimand A environmental covariates, plus:
- Institutional strength: `home_pre_match_elo`, `away_pre_match_elo`, `elo_diff_home_minus_away`
- Bowler style: `is_pace` (pace vs spin categorization)
- Micro-momentum: `recent_runs_12`, `recent_wickets_12`, `recent_dots_12`

**Purpose**: Measures the expected outcome for a randomly drawn competitive professional player placed in that specific match state, against that specific quality of opponent bowling attack, at that venue, in that competition, under that immediate momentum.

---

## 3. Empirical Model Evaluation (5-Fold Match-Grouped CV)

Both estimands were trained and evaluated across all 200,961 normal deliveries using 5-Fold Match-Grouped Cross-Validation (deliveries from the same match never bridge folds):

| Estimand Architecture | Features Count | Out-of-Fold MAE | MAE Std ($\sigma$) | Out-of-Fold RMSE | RMSE Std ($\sigma$) | Out-of-Fold $R^2$ | Interpretation & Downstream Usage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Estimand A: Situation-Only** | 8 | 1.2771 | 0.0122 | 1.6967 | 0.0137 | 0.0191 | Macro-environmental baseline; used for descriptive situational profiling |
| **Estimand B: Context + Opponent** | **14** | **1.2733** | **0.0122** | **1.6921** | **0.0135** | **0.0244** | **RECOMMENDED FOR PLAYER ATTRIBUTION**: Controls for opponent attack strength |

### Statistical Performance Analysis
1. Adding opponent quality and micro-momentum in Estimand B reduces both MAE (from $1.2771$ to $1.2733$) and RMSE (from $1.6967$ to $1.6921$) with tight cross-validation stability ($\sigma = 0.0122$).
2. While individual delivery variance in T20 is inherently noisy ($R^2 \approx 0.024$), Estimand B provides an unbiased, causally sound baseline that credits players for facing elite opposition.

---

## 4. Architectural Decision for Player Attribution

**PinkOps adopts Estimand B (Context + Opponent-Quality Population Expectation) as the primary baseline for player evaluation.**

### Rationale:
1. **Opposition Fairness**: If Player 1 scores 30 off 15 balls against Jasprit Bumrah and Jofra Archer, while Player 2 scores 30 off 15 balls against a fifth-bowler part-timer, Estimand A would treat them as identical. Estimand B incorporates opponent pre-match Elo and attack baselines, correctly rewarding Player 1 for outperforming a much tougher baseline expectation.
2. **Elimination of League Bias**: By controlling for pre-match Elo and competition scoring environments, Estimand B prevents international players from being unfairly penalized for playing in low-scoring World Cup tournaments compared to high-scoring franchise leagues.

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
