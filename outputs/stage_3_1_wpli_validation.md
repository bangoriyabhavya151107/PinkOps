# PinkOps — Stage 3.1: Win Probability Leverage Index (WPLI) Validation
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Output Data Reference**: [`data/processed/stage_3_1_wpli_comparison.csv`](file:///D:/PinkOps/data/processed/stage_3_1_wpli_comparison.csv)  
**Dataset Reference**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) (95,247 chase deliveries)  

---

## 1. Executive Summary & Audit Mandate

In Stage 3.0, the Win Probability Leverage Index ($\text{WPLI}$) was introduced as a candidate measure of match-state volatility. In Stage 3.1, this metric was subjected to independent review to answer critical methodological questions:
1. Are the counterfactual delivery states causally well-defined?
2. Is the normalization by $\sigma(\text{WP})$ statistically stable?
3. Does WPLI behave sensibly at extreme match states (e.g., blowouts vs. nail-biters)?
4. Does WPLI materially improve delivery-level expectation models, or is it better treated as a macro-level descriptive feature?

---

## 2. Counterfactual Definition & Mathematical Formulation

Let $\mathbf{X}(t^-) = [\text{RunsReq}, \text{BallsRem}, W_{\text{in\_hand}}, \text{TargetProx}, \text{Cushion}]$ represent the chase state immediately prior to delivery $t$.
A well-calibrated logistic win probability model estimates baseline win expectancy:
$$\text{WP}_0 = \sigma(\mathbf{w}^T \mathbf{X}(t^-))$$

We construct two **causally explicit counterfactual states** representing the two fundamental T20 delivery extremes:

### Counterfactual 1: The Wicket Event ($R = 0, W = 1$)
$$\mathbf{X}_{\text{wicket}} = [\text{RunsReq}, \text{BallsRem} - 1, W_{\text{in\_hand}} - 1, \dots]$$
$$\Delta \text{WP}_{\text{wicket}} = \max\left(0, \text{WP}_0 - \sigma(\mathbf{w}^T \mathbf{X}_{\text{wicket}})\right)$$
Measures the exact percentage-point loss in win probability if the batting team loses a wicket.

### Counterfactual 2: The Boundary Event ($R = 5, W = 0$)
$$\mathbf{X}_{\text{boundary}} = [\max(0, \text{RunsReq} - 5), \text{BallsRem} - 1, W_{\text{in\_hand}}, \dots]$$
$$\Delta \text{WP}_{\text{boundary}} = \max\left(0, \sigma(\mathbf{w}^T \mathbf{X}_{\text{boundary}}) - \text{WP}_0\right)$$
Measures the exact percentage-point gain in win probability if the batting team hits a boundary (modeled at 5 runs, the expectation between a four and a six).

---

## 3. Comparison of Three Candidate WPLI Formulations

We audited three mathematical formulations across all 95,247 chase deliveries:

| Formulation | Mathematical Definition | Min | P25 | Median | Mean | P75 | P95 | Max | Std | Spearman Corr ($B$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WPLI-A (Current Scaled)** | $\frac{\Delta \text{WP}_w + \Delta \text{WP}_b}{2 \cdot \sigma(\text{WP})}$ | 0.0000 | 0.0663 | 0.1926 | 0.1905 | 0.2938 | 0.3814 | 1.4484 | 0.1420 | **1.0000** |
| **WPLI-B (Absolute Swing)** | $\frac{1}{2}\left(|\Delta \text{WP}_w| + |\Delta \text{WP}_b|\right)$ | 0.0000 | 0.0229 | 0.0664 | 0.0657 | 0.1013 | 0.1315 | 0.4994 | 0.0490 | **1.0000** |
| **WPLI-C (RMS Leverage)** | $\sqrt{\frac{1}{2}\left(\Delta \text{WP}_w^2 + \Delta \text{WP}_b^2\right)}$ | 0.0000 | 0.0251 | 0.0749 | 0.0736 | 0.1155 | 0.1436 | 0.6463 | 0.0543 | **0.9955** |

### Critical Analytical Findings
1. **Mathematical Collinearity**: WPLI-A and WPLI-B are mathematically collinear ($r = 1.0000$). WPLI-A simply scales WPLI-B by a constant factor $\frac{1}{\sigma(\text{WP})} \approx 2.90$.
2. **Superiority of WPLI-B over WPLI-A**: WPLI-B is strictly bounded in $[0, 1]$ and represents an intuitive physical quantity: **the average percentage-point swing in match win probability on the next ball**.
   - An absolute swing of $0.0664$ (median) means the next ball swings win probability by $6.64$ percentage points.
   - A maximum swing of $0.4994$ means the delivery can swing the entire match outcome by $49.9$ percentage points!
3. **Behavior at Extreme Match States**:
   - **Blowout State (90 needed off 6 balls, 2 wkts)**: $\text{WP} = 0.000000 \implies \text{WPLI} = 0.0000$. The metric correctly registers zero leverage (the game is already decided).
   - **Easy Cruise State (10 needed off 60 balls, 9 wkts)**: $\text{WP} = 0.9977 \implies \text{WPLI} = 0.0012$. The metric correctly registers zero pressure.
   - **Balanced Death State (12 needed off 6 balls, 4 wkts)**: $\text{WP} = 0.6582 \implies \text{WPLI}_B = 0.3842$. Wicket drops WP to $0.32$, boundary pushes WP to $0.94$. The metric correctly captures peak drama.

---

## 4. Ablation Finding: Should WPLI Be a Primary Model Feature?

In our formal Pressure Component Ablation experiment (evaluating 200,961 deliveries via 5-Fold Match-Grouped CV):
- **Model C (Resource + Trajectory + Temporal/Rate)**: $\text{MAE} = 1.2811$ runs/ball.
- **Model D (Model C + WPLI)**: $\text{MAE} = 1.2810$ runs/ball.

**Empirical Result**: Adding WPLI to the delivery scoring model produces a negligible improvement of only **0.0001 runs/ball**!

### Why?
WPLI is a **macro-level win expectancy metric**, whereas delivery-level scoring is governed by **micro-level physics and rate pressure** (balls remaining, runs required, wickets in hand, phase, and bowler style). Win probability leverage does not dictate how a ball bounces; rather, rate pressure dictates batter risk-taking.

---

## 5. Architectural Recommendation & Verdict

**WPLI is officially DOWNGRADED from a primary model gate to a descriptive macro-level leverage feature.**

### Downstream Usage Protocol:
1. **Model Exclusion**: WPLI is **not** included as a primary feature in delivery expected-run models (avoiding unnecessary model complexity).
2. **Contextual Metadata**: WPLI-B is retained in the player evidence dataset as an uncollapsed descriptive metric, allowing decision-makers to filter and inspect player execution specifically in "High-Leverage Match-Winning Moments" ($\text{WPLI}_B \ge 0.15$).

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
