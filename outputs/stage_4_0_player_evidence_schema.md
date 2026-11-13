# PinkOps — Stage 4.0: Player Evidence Vector Schema & Field Dictionary

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_player_evidence_schema.md`  
**Stage:** 4.0 — Reliability Architecture, Estimand Freeze & Governance  
**Governance Status:** FROZEN SCHEMA (Zero Composite Scores / Zero Rankings)  

---

## 1. Schema Overview & Governance Mandate

This document defines the authoritative, uncollapsed **Player Evidence Vector Schema** for Operation Pink Panther. In accordance with the Stage 4.0 governance charter, this schema strictly prohibits single-score collapse. The evidence vector preserves the multi-dimensional structure of player performance across all seven architectural layers.

Downstream selection algorithms in Stage 4.1 must consume this vector in its uncollapsed form. Any attempt to introduce arbitrary linear weights, uncalibrated composite indices, or ad-hoc rankings violates the governance invariants of Operation Pink Panther.

---

## 2. Batter Evidence Vector Schema

| Layer | Field Name | Data Type | Mathematical Definition | Unit / Domain | Missingness Rule | Permitted Uses (Stage 4.1) | Prohibited Uses |
|---|---|---|---|---|---|---|---|
| **Identity** | `player_id` | `INT64` | Canonical analytical identifier | Unique ID | Non-nullable | Primary join key across telemetry | Do not use display name as key |
| **Identity** | `player_name` | `VARCHAR` | Display text representation | String | Non-nullable | Presentation and reporting | Joining, grouping, or matching |
| **L1: Opp** | `n_deliveries_total` | `INT64` | $\sum_{t \in \mathcal{D}_i} 1$ | Deliveries $\ge 0$ | Default 0 | Sample qualification, evidence tiering | Performance scoring |
| **L1: Opp** | `n_deliveries_pressure` | `INT64` | $\sum_{t \in \mathcal{D}_i} \mathbb{I}(P(t^-) \ge 0.50)$ | Deliveries $\ge 0$ | Default 0 | Pressure sample qualification | Standalone skill ranking |
| **L1: Opp** | `pressure_ratio` | `FLOAT64` | $N_{\text{press}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{total}} = 0$ | Exposure bias adjustment, role context | Standalone skill ranking |
| **L1: Opp** | `weighted_pressure_exposure` | `FLOAT64` | $\sum_{t \in \mathcal{D}_i} P(t^-)$ | Effective balls $\ge 0$ | 0.0 if $N_{\text{total}} = 0$ | Precision weighting, EB shrinkage | Standalone skill ranking |
| **L1: Opp** | `mean_pressure_faced` | `FLOAT64` | $\frac{1}{N} \sum_{t \in \mathcal{D}_i} P(t^-)$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{total}} = 0$ | Contextual leverage profile | Performance metric |
| **L2: Exp** | `mean_expected_runs` | `FLOAT64` | $\frac{1}{N} \sum_{t \in \mathcal{D}_i} \hat{\mu}_{\text{runs}}(t^-)$ | Runs / ball | NaN if $N = 0$ | Contextual expectation baseline | Individual player rating |
| **L2: Exp** | `mean_expected_runs_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum_{t \in \mathcal{D}_{i,\text{press}}} \hat{\mu}_{\text{runs}}(t^-)$ | Runs / ball | NaN if $N_{\text{press}} = 0$ | Pressure expectation baseline | Individual player rating |
| **L3: Exec** | `rva_per_ball_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum (\text{Runs}(t) - \hat{\mu}(t^-))$ | Runs / ball | 0.0 if $N_{\text{press}} = 0$ | Raw sample execution signal | Direct ranking without EB shrinkage |
| **L3: Exec** | `boundary_pct_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum \mathbb{I}(\text{Runs}(t) \in \{4, 6\})$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{press}} = 0$ | Boundary creation capability | Standalone selection |
| **L3: Exec** | `dot_pct_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum \mathbb{I}(\text{Runs}(t) = 0)$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{press}} = 0$ | Strike stagnation analysis | Standalone selection |
| **L3: Exec** | `strike_rate_pressure` | `FLOAT64` | $\frac{\text{Runs}_{\text{press}}}{N_{\text{press}}} \times 100$ | Runs / 100 balls | 0.0 if $N_{\text{press}} = 0$ | Traditional context benchmark | Uncontextualized ranking |
| **L4: Down** | `early_dismissal_rate` | `FLOAT64` | $\frac{\sum \mathbb{I}(\text{Out} \land \text{Balls} \le 5)}{\text{Innings}}$ | $[0.0, 1.0]$ | 0.0 if Innings = 0 | Catastrophe risk screening, hurdles | Linear weighting in composite |
| **L4: Down** | `pressure_collapse_rate` | `FLOAT64` | $\frac{\sum \mathbb{I}(\text{Out} \land \text{Runs} \le 5 \land P \ge 0.5)}{\text{PressureInnings}}$ | $[0.0, 1.0]$ | 0.0 if PressInnings = 0 | Critical failure screening | Linear weighting in composite |
| **L4: Cons** | `match_va_mad` | `FLOAT64` | $\text{median}(\|\text{VA}_m - \text{median}(\text{VA})\|)$ | Runs / match | 0.0 if Matches $\le 1$ | Volatility analysis, consistency filtering | Standalone selection |
| **L4: Cons** | `match_va_iqr` | `FLOAT64` | $Q_{0.75}(\text{VA}_m) - Q_{0.25}(\text{VA}_m)$ | Runs / match | 0.0 if Matches $\le 1$ | Interquartile dispersion | Standalone selection |
| **L4: Cons** | `negative_match_pct` | `FLOAT64` | $\frac{1}{M} \sum \mathbb{I}(\text{VA}_m < 0)$ | $[0.0, 1.0]$ | 0.0 if Matches = 0 | Negative outcome frequency | Standalone selection |
| **L4: Clut** | `clutch_delta_rva` | `FLOAT64` | $\overline{\text{RVA}}_{\text{press}} - \overline{\text{RVA}}_{\text{base}}$ (Phase-matched) | Runs / ball | 0.0 if sparse | Differential execution assessment | Unmatched comparisons |
| **L5: Unc** | `rva_eb_shrunk` | `FLOAT64` | $w_i \cdot \text{RVA}_i + (1 - w_i) \cdot \mu_0$ ($K=100$) | Runs / ball | 0.0 if $N_{\text{total}} = 0$ | Shrinkage-adjusted central estimate | Direct ranking without LCB |
| **L5: Unc** | `rva_se_eb` | `FLOAT64` | $\sqrt{\frac{\hat{\sigma}_i^2}{N^* + K} + \frac{K \cdot \sigma_0^2}{(N^* + K)^2}}$ | Runs / ball | $\sigma_0$ if $N = 0$ | Confidence bounds, interval estimation | Linear penalties |
| **L5: Unc** | `rva_lcb10` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 1.282 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | High-risk aversion screening | Sole selection criterion |
| **L5: Unc** | `rva_lcb20` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 0.842 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | **Primary conservative ranking signal** | Combining with ad-hoc bonuses |
| **L5: Unc** | `rva_lcb25` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 0.674 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | Multiverse robustness verification | Standalone ranking |
| **L5: Unc** | `rva_lcb30` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 0.524 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | Multiverse robustness verification | Standalone ranking |
| **L6: Cont** | `evidence_tier` | `VARCHAR` | Robust / Moderate / Sparse | Categorical | Sparse if $<50$ | Cohort gating, eligibility filtering | Rank sorting across tiers |
| **L6: Cont** | `pct_powerplay` | `FLOAT64` | $N_{\text{PP}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N = 0$ | Role classification (Opener) | Performance evaluation |
| **L6: Cont** | `pct_death` | `FLOAT64` | $N_{\text{Death}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N = 0$ | Role classification (Finisher) | Performance evaluation |
| **L6: Cont** | `pct_vs_pace` | `FLOAT64` | $N_{\text{Pace}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N = 0$ | Matchup / tactical suitability | Performance evaluation |
| **L6: Cont** | `mean_opp_elo_faced` | `FLOAT64` | $\frac{1}{N} \sum \text{Elo}_{\text{opp}}$ | Elo points $\approx 1500$ | 1500.0 if $N = 0$ | Competition quality audit | Arbitrary multiplier |
| **L6: Cont** | `super_over_balls` | `INT64` | Balls in Innings 3 & 4 | Deliveries $\ge 0$ | 0 if none | Qualitative stress-test audit | Inclusion in regression baselines |
| **L7: Dec** | `spec_b_rva_lcb20` | `FLOAT64` | LCB20 under Specification B | Runs / ball | 0.0 if sparse | Primary decision input | Arbitrary transformation |
| **L7: Dec** | `spec_a_rva_lcb20` | `FLOAT64` | LCB20 under Specification A | Runs / ball | 0.0 if sparse | Sensitivity & robustness check | Arbitrary transformation |

---

## 3. Bowler Evidence Vector Schema

| Layer | Field Name | Data Type | Mathematical Definition | Unit / Domain | Missingness Rule | Permitted Uses (Stage 4.1) | Prohibited Uses |
|---|---|---|---|---|---|---|---|
| **Identity** | `player_id` | `INT64` | Canonical analytical identifier | Unique ID | Non-nullable | Primary join key across telemetry | Do not use display name as key |
| **Identity** | `player_name` | `VARCHAR` | Display text representation | String | Non-nullable | Presentation and reporting | Joining, grouping, or matching |
| **L1: Opp** | `n_deliveries_total` | `INT64` | $\sum_{t \in \mathcal{D}_j} 1$ | Deliveries $\ge 0$ | Default 0 | Sample qualification, evidence tiering | Performance scoring |
| **L1: Opp** | `n_deliveries_pressure` | `INT64` | $\sum_{t \in \mathcal{D}_j} \mathbb{I}(P(t^-) \ge 0.50)$ | Deliveries $\ge 0$ | Default 0 | Pressure sample qualification | Standalone skill ranking |
| **L1: Opp** | `pressure_ratio` | `FLOAT64` | $N_{\text{press}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{total}} = 0$ | Exposure bias adjustment, role context | Standalone skill ranking |
| **L1: Opp** | `weighted_pressure_exposure` | `FLOAT64` | $\sum_{t \in \mathcal{D}_j} P(t^-)$ | Effective balls $\ge 0$ | 0.0 if $N_{\text{total}} = 0$ | Precision weighting, EB shrinkage | Standalone skill ranking |
| **L1: Opp** | `mean_pressure_bowled` | `FLOAT64` | $\frac{1}{N} \sum_{t \in \mathcal{D}_j} P(t^-)$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{total}} = 0$ | Contextual leverage profile | Performance metric |
| **L2: Exp** | `mean_expected_runs` | `FLOAT64` | $\frac{1}{N} \sum_{t \in \mathcal{D}_j} \hat{\mu}_{\text{runs}}(t^-)$ | Runs / ball | NaN if $N = 0$ | Contextual expectation baseline | Individual player rating |
| **L2: Exp** | `mean_expected_runs_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum_{t \in \mathcal{D}_{j,\text{press}}} \hat{\mu}_{\text{runs}}(t^-)$ | Runs / ball | NaN if $N_{\text{press}} = 0$ | Pressure expectation baseline | Individual player rating |
| **L3: Exec** | `rcs_per_ball_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum (\hat{\mu}(t^-) - \text{Runs}(t))$ | Runs / ball | 0.0 if $N_{\text{press}} = 0$ | Raw sample suppression signal | Direct ranking without EB shrinkage |
| **L3: Exec** | `dot_pct_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum \mathbb{I}(\text{Runs}(t) = 0)$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{press}} = 0$ | Dot pressure generation | Standalone selection |
| **L3: Exec** | `boundary_pct_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum \mathbb{I}(\text{Runs}(t) \in \{4, 6\})$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{press}} = 0$ | Boundary leakage analysis | Standalone selection |
| **L3: Exec** | `wicket_pct_pressure` | `FLOAT64` | $\frac{1}{N_{\text{press}}} \sum \mathbb{I}(\text{Wicket}(t) = 1)$ | $[0.0, 1.0]$ | 0.0 if $N_{\text{press}} = 0$ | Breakthrough capability | Standalone selection |
| **L3: Exec** | `economy_rate_pressure` | `FLOAT64` | $\frac{\text{RunsConceded}_{\text{press}}}{N_{\text{press}}} \times 6$ | Runs / over | 0.0 if $N_{\text{press}} = 0$ | Traditional context benchmark | Uncontextualized ranking |
| **L4: Down** | `blowout_over_rate` | `FLOAT64` | $\frac{\sum \mathbb{I}(\text{OverRuns} \ge 15)}{\text{TotalOvers}}$ | $[0.0, 1.0]$ | 0.0 if Overs = 0 | Catastrophe risk screening, hurdles | Linear weighting in composite |
| **L4: Down** | `pressure_blowout_rate` | `FLOAT64` | $\frac{\sum \mathbb{I}(\text{OverRuns} \ge 15 \land P_{\text{over}} \ge 0.5)}{\text{PressureOvers}}$ | $[0.0, 1.0]$ | 0.0 if PressOvers = 0 | Acute crisis blowout screening | Linear weighting in composite |
| **L4: Cons** | `match_va_mad` | `FLOAT64` | $\text{median}(\|\text{VA}_m - \text{median}(\text{VA})\|)$ | Runs / match | 0.0 if Matches $\le 1$ | Volatility analysis, consistency filtering | Standalone selection |
| **L4: Cons** | `match_va_iqr` | `FLOAT64` | $Q_{0.75}(\text{VA}_m) - Q_{0.25}(\text{VA}_m)$ | Runs / match | 0.0 if Matches $\le 1$ | Interquartile dispersion | Standalone selection |
| **L4: Cons** | `negative_match_pct` | `FLOAT64` | $\frac{1}{M} \sum \mathbb{I}(\text{VA}_m < 0)$ | $[0.0, 1.0]$ | 0.0 if Matches = 0 | Negative outcome frequency | Standalone selection |
| **L4: Clut** | `clutch_delta_rcs` | `FLOAT64` | $\overline{\text{RCS}}_{\text{press}} - \overline{\text{RCS}}_{\text{base}}$ (Phase-matched) | Runs / ball | 0.0 if sparse | Differential execution assessment | Unmatched comparisons |
| **L5: Unc** | `rcs_eb_shrunk` | `FLOAT64` | $w_j \cdot \text{RCS}_j + (1 - w_j) \cdot \mu_0$ ($K=100$) | Runs / ball | 0.0 if $N_{\text{total}} = 0$ | Shrinkage-adjusted central estimate | Direct ranking without LCB |
| **L5: Unc** | `rcs_se_eb` | `FLOAT64` | $\sqrt{\frac{\hat{\sigma}_j^2}{N^* + K} + \frac{K \cdot \sigma_0^2}{(N^* + K)^2}}$ | Runs / ball | $\sigma_0$ if $N = 0$ | Confidence bounds, interval estimation | Linear penalties |
| **L5: Unc** | `rcs_lcb10` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 1.282 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | High-risk aversion screening | Sole selection criterion |
| **L5: Unc** | `rcs_lcb20` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 0.842 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | **Primary conservative ranking signal** | Combining with ad-hoc bonuses |
| **L5: Unc** | `rcs_lcb25` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 0.674 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | Multiverse robustness verification | Standalone ranking |
| **L5: Unc** | `rcs_lcb30` | `FLOAT64` | $\hat{\theta}^{\text{EB}} - 0.524 \cdot \text{SE}$ | Runs / ball | 0.0 if $N = 0$ | Multiverse robustness verification | Standalone ranking |
| **L6: Cont** | `evidence_tier` | `VARCHAR` | Robust / Moderate / Sparse | Categorical | Sparse if $<50$ | Cohort gating, eligibility filtering | Rank sorting across tiers |
| **L6: Cont** | `pct_powerplay` | `FLOAT64` | $N_{\text{PP}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N = 0$ | Role classification (Powerplay specialist) | Performance evaluation |
| **L6: Cont** | `pct_death` | `FLOAT64` | $N_{\text{Death}} / N_{\text{total}}$ | $[0.0, 1.0]$ | 0.0 if $N = 0$ | Role classification (Death specialist) | Performance evaluation |
| **L6: Cont** | `mean_opp_elo_faced` | `FLOAT64` | $\frac{1}{N} \sum \text{Elo}_{\text{opp}}$ | Elo points $\approx 1500$ | 1500.0 if $N = 0$ | Competition quality audit | Arbitrary multiplier |
| **L6: Cont** | `super_over_balls` | `INT64` | Balls in Innings 3 & 4 | Deliveries $\ge 0$ | 0 if none | Qualitative stress-test audit | Inclusion in regression baselines |
| **L7: Dec** | `spec_b_rcs_lcb20` | `FLOAT64` | LCB20 under Specification B | Runs / ball | 0.0 if sparse | Primary decision input | Arbitrary transformation |
| **L7: Dec** | `spec_a_rcs_lcb20` | `FLOAT64` | LCB20 under Specification A | Runs / ball | 0.0 if sparse | Sensitivity & robustness check | Arbitrary transformation |

---

## 4. Anti-Collapse Verification & Missingness Protocols

1. **Zero Composite Columns:** Programmatic verification confirms the complete absence of `rank`, `pinkops_score`, `composite_score`, or `total_score` fields.
2. **Missingness Preservation:** When a player has zero exposure in a subset (e.g., $N_{\text{press}} = 0$), execution metrics are imputed as neutral prior expectations ($0.0$) while the uncertainty standard error expands to the prior standard deviation ($\sigma_0$). This naturally forces the LCB downward without needing arbitrary sentinel values.
3. **Immutability:** The field names, types, and mathematical formulas specified in this document are frozen for Stage 4.1 consumption.

*Document Approved by PinkOps Quantitative Governance Committee.*
