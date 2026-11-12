# PinkOps — Stage 3.0: Pressure Variable Audit Report
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Dataset**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) (200,999 deliveries, 867 matches)  
**Output Data Reference**: [`data/processed/pressure_variable_stats.csv`](file:///D:/PinkOps/data/processed/pressure_variable_stats.csv)  

---

## 1. Executive Summary & Audit Mandate

In strict accordance with Stage 3 directives:
- **Pressure must be continuous**, rejecting naive binary classifications ($\text{pressure} \in \{0, 1\}$).
- **Situation difficulty (environment) must be decoupled from player outcome (performance)**.
- **Every candidate variable must be audited for data availability, missingness, distribution, potential data leakage, and cricket validity before inclusion in models.**

This audit evaluates **14 continuous pressure variables** extracted from the canonical match-state dataset.

---

## 2. Comprehensive Variable Audit Registry

| Variable Name | Scope | Null Count | Null % | Min | P25 | Median | P75 | Max | Leakage Status | Stage 3 Suitability |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `runs_required_before` | Innings 2 & 4 | 105,752 | 52.61% | 0.00 | 59.00 | 100.00 | 142.00 | 305.00 | **LEAKAGE-FREE** | Approved (Chase models) |
| `balls_remaining_before` | Universal | 0 | 0.00% | 1.00 | 33.00 | 63.00 | 92.00 | 120.00 | **LEAKAGE-FREE** | Approved (Universal) |
| `required_run_rate_before` | Chase ($B > 0$) | 105,752 | 52.61% | 0.00 | 7.62 | 9.60 | 12.00 | 900.00 | **LEAKAGE-FREE** | Approved (Requires transform) |
| `current_run_rate_before` | Historical ($B > 0$) | 1,843 | 0.92% | 0.00 | 6.80 | 8.22 | 9.76 | 78.00 | **LEAKAGE-FREE** | Approved (Universal) |
| `rrr_crr_delta_before` | Chase ($B > 0$) | 106,647 | 53.06% | -51.88 | -1.37 | 1.63 | 4.84 | 892.54 | **LEAKAGE-FREE** | Approved (Chase stress) |
| `wickets_in_hand_before` | Universal | 0 | 0.00% | 1.00 | 6.00 | 8.00 | 9.00 | 10.00 | **LEAKAGE-FREE** | Approved (Universal) |
| `wickets_before` | Universal | 0 | 0.00% | 0.00 | 1.00 | 2.00 | 4.00 | 9.00 | **LEAKAGE-FREE** | Approved (Universal) |
| `innings_progress_before` | Universal | 0 | 0.00% | 0.00 | 0.23 | 0.48 | 0.72 | 0.99 | **LEAKAGE-FREE** | Approved (Universal) |
| `recent_runs_12` | Preceding 12 balls | 0 | 0.00% | 0.00 | 11.00 | 15.00 | 21.00 | 58.00 | **LEAKAGE-FREE** | Approved (Micro-momentum) |
| `recent_wickets_12` | Preceding 12 balls | 0 | 0.00% | 0.00 | 0.00 | 0.00 | 1.00 | 6.00 | **LEAKAGE-FREE** | Approved (Acute collapse) |
| `recent_dots_12` | Preceding 12 balls | 0 | 0.00% | 0.00 | 2.00 | 4.00 | 5.00 | 12.00 | **LEAKAGE-FREE** | Approved (Strangulation) |
| `resource_depletion_index` | Universal (1st Inn) | 0 | 0.00% | 0.00 | 1.94 | 3.79 | 5.54 | 18.18 | **LEAKAGE-FREE** | Approved (1st Inn crisis) |
| `balls_per_wicket_cushion` | Universal | 0 | 0.00% | 0.10 | 5.18 | 8.11 | 10.29 | 42.67 | **LEAKAGE-FREE** | Approved (Universal) |
| `target_proximity` | Chase | 105,752 | 52.61% | 0.00 | 1.25 | 1.57 | 1.95 | 75.00 | **LEAKAGE-FREE** | Approved (Numerical stability) |

---

## 3. Deep-Dive Variable Profiles & Cricket Interpretation

### 1. `runs_required_before`
- **Definition**: Target runs minus total runs scored before the delivery: $\max(0, T - R_{\text{before}})$.
- **Availability**: Strictly defined in 2nd and 4th innings (chases). Null in 1st Innings (105,727 balls) and 25 balls of match 35003 where chase did not commence.
- **Distribution**: Interquartile range spans 59 to 142 runs. Median is 100.0 runs. Max is 305 runs (extreme international chases).
- **Leakage Assessment**: **Zero leakage.** Strictly computed from cumulative runs prior to delivery.
- **Cricket Interpretation**: Captures total distance to the finish line. A batter facing 10 runs required is in a vastly different tactical posture than one facing 150 runs required.
- **Stage 3 Recommendation**: **APPROVED** for Chase Expectation and Leverage models.

### 2. `balls_remaining_before`
- **Definition**: Scheduled legal balls minus legal balls bowled: $B_{\text{scheduled}} - B_{\text{bowled}}$.
- **Availability**: 100% complete across all 200,999 deliveries (0 nulls). Bounded $[1, 120]$ (except shortened matches and Super Overs where $B_{\text{scheduled}} \in [6, 114]$).
- **Distribution**: Uniformly distributed across normal innings ($P25 = 33, \text{Median} = 63, P75 = 92$).
- **Leakage Assessment**: **Zero leakage.** Derived strictly from prior legal deliveries.
- **Cricket Interpretation**: Fundamental temporal resource denominator. Dictates how many deliveries remain to distribute risk.
- **Stage 3 Recommendation**: **APPROVED** as universal covariate.

### 3. `required_run_rate_before` (RRR)
- **Definition**: Normalized scoring rate required to win: $\text{RRR} = \frac{\text{runs\_required}}{\text{balls\_remaining} / 6.0}$.
- **Availability**: 95,247 chase deliveries.
- **Distributional Anomaly Discovered**: Median is 9.60, mean is 11.40, but **maximum reaches 900.00**!
  - *Cause*: When 15 runs are needed off 1 ball, $\text{RRR} = 15 / (1/6) = 90.00$. When 150 runs are needed off 1 ball in an impossible chase, $\text{RRR} = 900.00$.
- **Leakage Assessment**: **Zero leakage.**
- **Analytical Warning**: **Raw RRR cannot be used directly in unregularized linear models** due to asymptotic explosion as $B_{\text{remaining}} \to 0$.
- **Stage 3 Recommendation**: **APPROVED WITH TRANSFORMATION**. Must be clamped at $\text{RRR} \le 36.0$ or transformed via log-scaling:
  $$\text{RRR}_{\text{scaled}} = \log\left(1 + \min(\text{RRR}, 36.0)\right)$$
  or replaced by `target_proximity` ($\text{runs} / (\text{balls} + 1)$).

### 4. `current_run_rate_before` (CRR)
- **Definition**: Cumulative runs scored per over bowled: $\frac{R_{\text{before}}}{B_{\text{bowled}} / 6.0}$.
- **Availability**: 99.08% complete (1,843 nulls corresponding strictly to ball 1 of each innings where $B_{\text{bowled}} = 0$).
- **Distribution**: Min = 0.00, Median = 8.22, P75 = 9.76. Max reaches 78.00 in ultra-early overs (e.g., 13 off 1 legal ball).
- **Leakage Assessment**: **Zero leakage.**
- **Cricket Interpretation**: Measures batting team's established scoring pace.
- **Stage 3 Recommendation**: **APPROVED**. Missing values on ball 1 imputed to competition/venue baseline scoring rate.

### 5. `rrr_crr_delta_before`
- **Definition**: $\text{RRR}_{\text{before}} - \text{CRR}_{\text{before}}$.
- **Availability**: 94,352 chase deliveries where both RRR and CRR are defined.
- **Distribution**: Median is $+1.63$ (chasing teams on average trail required pace). Spans from $-51.88$ (comfortably ahead) to $+892.54$ (mathematical impossibility).
- **Leakage Assessment**: **Zero leakage.**
- **Cricket Interpretation**: Captures the *acceleration gradient*. A high positive delta indicates that the batting team has fallen behind the clock and must immediately take elevated risks.
- **Stage 3 Recommendation**: **APPROVED WITH CLAMPING** $[-10.0, +25.0]$.

### 6. `wickets_in_hand_before` & `wickets_before`
- **Definition**: Wickets remaining before all-out ($10 - W_{\text{lost}}$ in normal innings; $2 - W_{\text{lost}}$ in Super Overs).
- **Availability**: 100% complete (0 nulls). Range $[1, 10]$ in normal innings; $[1, 2]$ in Super Overs.
- **Distribution**: Median = 8 wickets in hand, P25 = 6, Min = 1 (last pair at crease).
- **Leakage Assessment**: **Zero leakage.**
- **Cricket Interpretation**: The primary constraint on risk-taking. Teams with 8 wickets in hand can afford high-variance boundary-hunting; teams with 2 wickets in hand must protect against immediate match termination.
- **Stage 3 Recommendation**: **APPROVED** as foundational state variable.

### 7. `recent_runs_12`, `recent_wickets_12`, `recent_dots_12` (Rolling Pre-Delivery Context)
- **Definition**: Window functions over preceding 12 balls within the same match and innings:
  `ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING`
- **Availability**: 100% complete (coalesced to 0 for initial deliveries of innings).
- **Empirical Distributions**:
  - `recent_runs_12`: Median = 15.0 (run rate 7.50), P75 = 21.0, Max = 58.0 (consecutive explosive overs).
  - `recent_wickets_12`: Median = 0.0, Mean = 0.57, Max = 6.0 (devastating multi-wicket collapse).
  - `recent_dots_12`: Median = 4.0, Mean = 3.86, Max = 12.0 (back-to-back maiden overs).
- **Leakage Assessment**: **Zero leakage.** By explicitly setting the window frame to end at `1 PRECEDING`, the current delivery outcome is strictly excluded.
- **Cricket Interpretation**: Captures live psychological momentum and micro-match dynamics that static over counts miss. A batter walking in at 50/3 after 2 wickets in the last 4 balls faces acute shock pressure.
- **Stage 3 Recommendation**: **APPROVED** as dynamic state covariates.

### 8. `resource_depletion_index` (First-Innings Crisis Feature)
- **Definition**: Wickets lost relative to temporal progress:
  $$\text{RDI}(t^-) = \frac{\text{wickets\_before}}{\text{innings\_progress\_before} + 0.15}$$
- **Availability**: 100% complete across all deliveries (0 nulls).
- **Distribution**: Median = 3.79, P75 = 5.54, Max = 18.18.
- **Leakage Assessment**: **Zero leakage.**
- **Cricket Interpretation**: **Solves the first-innings pressure dilemma**. In the first innings, there is no RRR to signal pressure. RDI provides an objective, empirical measure of batting crisis:
  - Team at 20/3 after 3 overs: $\text{Progress} = 0.15 \implies \text{RDI} = 3 / (0.15 + 0.15) = 10.0$ (**Acute Crisis**).
  - Team at 160/3 after 17 overs: $\text{Progress} = 0.85 \implies \text{RDI} = 3 / (0.85 + 0.15) = 3.0$ (**Comfortable Platform**).
- **Stage 3 Recommendation**: **APPROVED** as primary First-Innings Crisis Indicator.

### 9. `balls_per_wicket_cushion`
- **Definition**: $\frac{\text{balls\_remaining\_before}}{\text{wickets\_in_hand\_before} + 0.5}$.
- **Availability**: 100% complete (0 nulls). Range $[0.10, 42.67]$. Median = 8.11 balls per wicket.
- **Leakage Assessment**: **Zero leakage.**
- **Cricket Interpretation**: Measures the resource buffer. If a team has 6 balls per wicket remaining, every batter can afford to spend 6 balls; if the buffer drops below 2.0 balls per wicket, the team is in immediate survival mode.
- **Stage 3 Recommendation**: **APPROVED** as continuous risk-cushion metric.

### 10. `target_proximity`
- **Definition**: $\frac{\text{runs\_required\_before}}{\text{balls\_remaining\_before} + 1.0}$.
- **Availability**: 95,247 chase deliveries.
- **Distribution**: Median = 1.57 runs/ball, P75 = 1.95 runs/ball, Max = 75.00.
- **Leakage Assessment**: **Zero leakage.**
- **Cricket Interpretation**: Normalized required scoring density per delivery. It possesses superior mathematical stability over RRR because the $+1.0$ denominator prevents division-by-zero singularities.
- **Stage 3 Recommendation**: **APPROVED** as preferred numerical replacement for raw RRR in regression pipelines.

---

## 4. Continuous Pressure Formulations

To ensure that pressure is evaluated continuously rather than through arbitrary binary gates, we establish two empirical formulations:

### Formulation A: Chase Pressure Intensity ($P_{\text{chase}}$)
In chases, pressure intensity is a function of Leverage and Rate Deficit:
$$P_{\text{chase}}(t^-) = \omega_1 \cdot \text{WPLI}(t^-) + \omega_2 \cdot \frac{\text{TargetProximity}(t^-)}{\text{BaselineRate}} + \omega_3 \cdot \frac{1}{\text{BallsPerWicketCushion}(t^-)}$$
where $\text{WPLI}$ is the Win Probability Leverage Index.

### Formulation B: First-Innings Pressure Intensity ($P_{\text{inn1}}$)
In the first innings, pressure intensity is a function of Resource Crisis and Death Urgency:
$$P_{\text{inn1}}(t^-) = \alpha_1 \cdot \frac{\text{RDI}(t^-)}{\overline{\text{RDI}}} + \alpha_2 \cdot \mathbb{I}(\text{DeathPhase}) \cdot \left(\frac{\text{BallsRemaining}(t^-)}{W_{\text{in\_hand}}(t^-) + 0.5}\right)^{-1}$$

*(Note: Parameters $\omega$ and $\alpha$ are normalized empirically to produce a continuous index bounded $[0, 1]$; no subjective rankings are created).*

---

## 5. Audit Conclusion & Suitability Decision

All 14 audited variables satisfy the **Strict Pre-Delivery Invariant**.
- Zero data leakage detected.
- Raw RRR requires log/clamping transformation.
- All candidate features are mathematically validated for Stage 3 expected outcome modeling.

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
