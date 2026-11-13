# PinkOps — Stage 5: Player Evidence Table Data Dictionary
**Project:** Operation Pink Panther / PinkOps  
**Stage:** Stage 5 Squad Assembly & Final Player Selection  
**Dataset Artifact:** [`data/processed/stage_5_player_evidence.parquet`](file:///D:/PinkOps/data/processed/stage_5_player_evidence.parquet)  
**Total Records:** 1,535 (888 Batters, 647 Bowlers)  
**Total Dimensions:** 75  

---

## 1. Dimensional Architecture

The Stage 5 Player Evidence Table encapsulates the uncollapsed, multi-dimensional performance, reliability, uncertainty, risk, and contextual footprint of every player appearing in the 2022+ competition dataset.

| Dimension Group | Core Fields | Description &
 Governing Principle |
| :--- | :--- | :--- |
| **Identity** | `player_id`, `player_name`, `role`, `teams`, `competitions`, `seasons` | Canonical player identifiers and participation scope across IPL and T20Is. |
| **Exposure** | `n_deliveries_total`, `n_deliveries_pressure`, `chase_deliveries`, `first_innings_deliveries`, `powerplay_deliveries`, `death_deliveries` | Volume of competitive opportunities faced or bowled across innings phases and game states. |
| **Performance** | `actual_runs`, `expected_runs`, `value_added_total`, `actual_runs_conceded`, `run_prevention_total`, `bowler_wickets` | Context-adjusted scoring and containment relative to the Spec B expectation model. |
| **Pressure** | `rva_per_ball_pressure`, `pressure_ratio`, `weighted_pressure_exposure`, `clutch_delta_rva` | Empirical value-added per delivery in top-quintile pressure leverage ($	ext{PI}_{80} \ge 0.5898$) and matched CEM contrasts. |
| **Reliability** | `eb_shrunk_estimate`, `se_eb`, `lub_10`, `lub_20`, `lub_25`, `lub_30`, `match_va_mad`, `match_va_iqr`, `negative_match_pct` | Empirical Bayes shrinkage ($K=100$) and lower uncertainty bounds penalizing small samples without rank distortion. |
| **Context** | `pct_powerplay`, `pct_death`, `pct_vs_pace`, `mean_opp_elo_faced`, `tactical_role` | Environmental, opposition strength, and tactical situational baselines. |
| **Risk** | `early_dismissal_rate`, `pressure_collapse_rate`, `downside_risk_rate`, `uncertainty_tier` | Quantified failure probabilities and standard errors protecting against downside fragility. |
| **Robustness** | `multiverse_specs_supported`, `multiverse_support_pct`, `robustness_tier` | Invariance of player signal across 15 independent methodological multiverse specifications. |
| **Evidence Tiers** | `evidence_tier`, `exposure_tier`, `reliability_profile` | Governance categorizations preventing false precision on low-sample records. |

---

## 2. Comprehensive Field Registry

| Column Name | Type | Description | Source / Provenance |
| :--- | :--- | :--- | :--- |
| `player_id` | `int64` | Contextual dimension for player_id (e.g. `8`) | `match_state.parquet` / Stage 4.1.1 |
| `player_name` | `str` | Contextual dimension for player_name (e.g. `Mahendra Singh Dhoni`) | `match_state.parquet` / Stage 4.1.1 |
| `role` | `str` | Contextual dimension for role (e.g. `batter`) | `match_state.parquet` / Stage 4.1.1 |
| `n_deliveries_total` | `int64` | Contextual dimension for n_deliveries_total (e.g. `497`) | `match_state.parquet` / Stage 4.1.1 |
| `n_deliveries_pressure` | `int64` | Contextual dimension for n_deliveries_pressure (e.g. `419`) | `match_state.parquet` / Stage 4.1.1 |
| `pressure_ratio` | `float64` | Contextual dimension for pressure_ratio (e.g. `0.8431`) | `match_state.parquet` / Stage 4.1.1 |
| `weighted_pressure_exposure` | `float64` | Contextual dimension for weighted_pressure_exposure (e.g. `351.0909`) | `match_state.parquet` / Stage 4.1.1 |
| `mean_pressure_faced` | `float64` | Contextual dimension for mean_pressure_faced (e.g. `0.7064`) | `match_state.parquet` / Stage 4.1.1 |
| `mean_expected_runs` | `float64` | Contextual dimension for mean_expected_runs (e.g. `1.4672`) | `match_state.parquet` / Stage 4.1.1 |
| `mean_expected_runs_pressure` | `float64` | Contextual dimension for mean_expected_runs_pressure (e.g. `1.4464`) | `match_state.parquet` / Stage 4.1.1 |
| `rva_per_ball_pressure` | `float64` | Contextual dimension for rva_per_ball_pressure (e.g. `-0.0455`) | `match_state.parquet` / Stage 4.1.1 |
| `boundary_pct_pressure` | `float64` | Contextual dimension for boundary_pct_pressure (e.g. `0.1911`) | `match_state.parquet` / Stage 4.1.1 |
| `dot_pct_pressure` | `float64` | Contextual dimension for dot_pct_pressure (e.g. `0.34`) | `match_state.parquet` / Stage 4.1.1 |
| `strike_rate_pressure` | `float64` | Contextual dimension for strike_rate_pressure (e.g. `140.1`) | `match_state.parquet` / Stage 4.1.1 |
| `early_dismissal_rate` | `float64` | Contextual dimension for early_dismissal_rate (e.g. `0.1458`) | `match_state.parquet` / Stage 4.1.1 |
| `pressure_collapse_rate` | `float64` | Contextual dimension for pressure_collapse_rate (e.g. `0.125`) | `match_state.parquet` / Stage 4.1.1 |
| `match_va_mad` | `float64` | Contextual dimension for match_va_mad (e.g. `0.6581`) | `match_state.parquet` / Stage 4.1.1 |
| `match_va_iqr` | `float64` | Contextual dimension for match_va_iqr (e.g. `1.3539`) | `match_state.parquet` / Stage 4.1.1 |
| `negative_match_pct` | `float64` | Contextual dimension for negative_match_pct (e.g. `0.6042`) | `match_state.parquet` / Stage 4.1.1 |
| `clutch_delta_rva` | `float64` | Contextual dimension for clutch_delta_rva (e.g. `0.5369`) | `match_state.parquet` / Stage 4.1.1 |
| `eb_shrunk_estimate` | `float64` | Contextual dimension for eb_shrunk_estimate (e.g. `-0.0367`) | `match_state.parquet` / Stage 4.1.1 |
| `se_eb` | `float64` | Contextual dimension for se_eb (e.g. `0.0527`) | `match_state.parquet` / Stage 4.1.1 |
| `lub_10` | `float64` | Contextual dimension for lub_10 (e.g. `-0.1043`) | `match_state.parquet` / Stage 4.1.1 |
| `lub_20` | `float64` | Contextual dimension for lub_20 (e.g. `-0.0811`) | `match_state.parquet` / Stage 4.1.1 |
| `lub_25` | `float64` | Contextual dimension for lub_25 (e.g. `-0.0723`) | `match_state.parquet` / Stage 4.1.1 |
| `lub_30` | `float64` | Contextual dimension for lub_30 (e.g. `-0.0644`) | `match_state.parquet` / Stage 4.1.1 |
| `lcb_20` | `float64` | Contextual dimension for lcb_20 (e.g. `-0.0811`) | `match_state.parquet` / Stage 4.1.1 |
| `evidence_tier` | `str` | Contextual dimension for evidence_tier (e.g. `Robust Evidence`) | `match_state.parquet` / Stage 4.1.1 |
| `pct_powerplay` | `float64` | Contextual dimension for pct_powerplay (e.g. `0.0141`) | `match_state.parquet` / Stage 4.1.1 |
| `pct_death` | `float64` | Contextual dimension for pct_death (e.g. `0.8209`) | `match_state.parquet` / Stage 4.1.1 |
| `pct_vs_pace` | `float64` | Contextual dimension for pct_vs_pace (e.g. `0.6942`) | `match_state.parquet` / Stage 4.1.1 |
| `mean_opp_elo_faced` | `float64` | Contextual dimension for mean_opp_elo_faced (e.g. `1494.2`) | `match_state.parquet` / Stage 4.1.1 |
| `super_over_balls` | `int64` | Contextual dimension for super_over_balls (e.g. `0`) | `match_state.parquet` / Stage 4.1.1 |
| `spec_b_lub20` | `float64` | Contextual dimension for spec_b_lub20 (e.g. `-0.0811`) | `match_state.parquet` / Stage 4.1.1 |
| `spec_a_lub20` | `float64` | Contextual dimension for spec_a_lub20 (e.g. `-0.0877`) | `match_state.parquet` / Stage 4.1.1 |
| `tactical_role` | `str` | Contextual dimension for tactical_role (e.g. `Finisher / Death Specialist`) | `match_state.parquet` / Stage 4.1.1 |
| `reliability_profile` | `str` | Contextual dimension for reliability_profile (e.g. `Pressure Concern`) | `match_state.parquet` / Stage 4.1.1 |
| `classification_rationale` | `str` | Contextual dimension for classification_rationale (e.g. `Supported negative execution (LUB20: ...`) | `match_state.parquet` / Stage 4.1.1 |
| `multiverse_specs_supported` | `int64` | Contextual dimension for multiverse_specs_supported (e.g. `0`) | `match_state.parquet` / Stage 4.1.1 |
| `multiverse_support_pct` | `float64` | Contextual dimension for multiverse_support_pct (e.g. `0.0`) | `match_state.parquet` / Stage 4.1.1 |
| `teams` | `str` | Contextual dimension for teams (e.g. `1`) | `match_state.parquet` / Stage 4.1.1 |
| `competitions` | `str` | Contextual dimension for competitions (e.g. `IPL 2022, IPL 2023, IPL 2024, IPL 2025`) | `match_state.parquet` / Stage 4.1.1 |
| `seasons` | `str` | Contextual dimension for seasons (e.g. `2022, 2023, 2024, 2025`) | `match_state.parquet` / Stage 4.1.1 |
| `actual_runs` | `float64` | Contextual dimension for actual_runs (e.g. `684.0`) | `match_state.parquet` / Stage 4.1.1 |
| `boundary_runs` | `float64` | Contextual dimension for boundary_runs (e.g. `464.0`) | `match_state.parquet` / Stage 4.1.1 |
| `dot_balls_faced` | `float64` | Contextual dimension for dot_balls_faced (e.g. `166.0`) | `match_state.parquet` / Stage 4.1.1 |
| `rotation_balls_faced` | `float64` | Contextual dimension for rotation_balls_faced (e.g. `197.0`) | `match_state.parquet` / Stage 4.1.1 |
| `chase_deliveries` | `float64` | Contextual dimension for chase_deliveries (e.g. `218.0`) | `match_state.parquet` / Stage 4.1.1 |
| `first_innings_deliveries` | `float64` | Contextual dimension for first_innings_deliveries (e.g. `239.0`) | `match_state.parquet` / Stage 4.1.1 |
| `powerplay_deliveries` | `float64` | Contextual dimension for powerplay_deliveries (e.g. `5.0`) | `match_state.parquet` / Stage 4.1.1 |
| `middle_deliveries` | `float64` | Contextual dimension for middle_deliveries (e.g. `107.0`) | `match_state.parquet` / Stage 4.1.1 |
| `death_deliveries` | `float64` | Contextual dimension for death_deliveries (e.g. `345.0`) | `match_state.parquet` / Stage 4.1.1 |
| `times_dismissed` | `float64` | Contextual dimension for times_dismissed (e.g. `24.0`) | `match_state.parquet` / Stage 4.1.1 |
| `matches_batted` | `float64` | Contextual dimension for matches_batted (e.g. `48.0`) | `match_state.parquet` / Stage 4.1.1 |
| `expected_runs` | `float64` | Contextual dimension for expected_runs (e.g. `729.2`) | `match_state.parquet` / Stage 4.1.1 |
| `value_added_total` | `float64` | Contextual dimension for value_added_total (e.g. `-45.2`) | `match_state.parquet` / Stage 4.1.1 |
| `boundary_run_pct` | `float64` | Contextual dimension for boundary_run_pct (e.g. `0.6784`) | `match_state.parquet` / Stage 4.1.1 |
| `dot_ball_pct` | `float64` | Contextual dimension for dot_ball_pct (e.g. `0.334`) | `match_state.parquet` / Stage 4.1.1 |
| `strike_rotation_pct` | `float64` | Contextual dimension for strike_rotation_pct (e.g. `0.3964`) | `match_state.parquet` / Stage 4.1.1 |
| `wicket_preservation_pct` | `float64` | Contextual dimension for wicket_preservation_pct (e.g. `0.9517`) | `match_state.parquet` / Stage 4.1.1 |
| `actual_runs_conceded` | `float64` | Contextual dimension for actual_runs_conceded (e.g. `807.0`) | `match_state.parquet` / Stage 4.1.1 |
| `bowler_wickets` | `float64` | Contextual dimension for bowler_wickets (e.g. `35.0`) | `match_state.parquet` / Stage 4.1.1 |
| `dot_balls_bowled` | `float64` | Contextual dimension for dot_balls_bowled (e.g. `185.0`) | `match_state.parquet` / Stage 4.1.1 |
| `boundaries_conceded` | `float64` | Contextual dimension for boundaries_conceded (e.g. `95.0`) | `match_state.parquet` / Stage 4.1.1 |
| `discipline_extras` | `float64` | Contextual dimension for discipline_extras (e.g. `0.0`) | `match_state.parquet` / Stage 4.1.1 |
| `matches_bowled` | `float64` | Contextual dimension for matches_bowled (e.g. `27.0`) | `match_state.parquet` / Stage 4.1.1 |
| `expected_runs_conceded` | `float64` | Contextual dimension for expected_runs_conceded (e.g. `811.1`) | `match_state.parquet` / Stage 4.1.1 |
| `run_prevention_total` | `float64` | Contextual dimension for run_prevention_total (e.g. `4.1`) | `match_state.parquet` / Stage 4.1.1 |
| `wicket_strike_rate` | `float64` | Contextual dimension for wicket_strike_rate (e.g. `16.74`) | `match_state.parquet` / Stage 4.1.1 |
| `boundary_conceded_pct` | `float64` | Contextual dimension for boundary_conceded_pct (e.g. `0.1621`) | `match_state.parquet` / Stage 4.1.1 |
| `discipline_extras_rate` | `float64` | Contextual dimension for discipline_extras_rate (e.g. `0.0`) | `match_state.parquet` / Stage 4.1.1 |
| `uncertainty_tier` | `str` | Contextual dimension for uncertainty_tier (e.g. `Low Uncertainty`) | `match_state.parquet` / Stage 4.1.1 |
| `exposure_tier` | `str` | Contextual dimension for exposure_tier (e.g. `Very High Exposure`) | `match_state.parquet` / Stage 4.1.1 |
| `robustness_tier` | `str` | Contextual dimension for robustness_tier (e.g. `Fragile / Low Support (<3/6)`) | `match_state.parquet` / Stage 4.1.1 |
| `downside_risk_rate` | `float64` | Contextual dimension for downside_risk_rate (e.g. `0.1458`) | `match_state.parquet` / Stage 4.1.1 |

---

*End of Stage 5 Player Evidence Table Data Dictionary.*
