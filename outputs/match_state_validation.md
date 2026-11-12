# Match-State Validation Report: Operation Pink Panther
**Project**: Rajasthan Royals SupeRR Selector Season 2 - Round 1  
**Brand**: PinkOps  
**Pipeline Stage**: Stage 2.1 (Hardened Match-State Construction)  
**Date Generated**: 2026-11-12 20:13:59  
**Source Table**: `data/raw/ball_by_ball.csv` (200,999 deliveries)  
**Processed Table**: `data/processed/match_state.parquet`  

> [!IMPORTANT]
> Stage 2.1 hardens the delivery-level match-state table with strict semantic validation, leakage prevention, and explicit scope separation. **No pressure engine, weights, thresholds, or player rankings** have been introduced.

---

## 1. Executive Summary & Verification Metrics

| Metric | Value | Verification Status |
| :--- | :--- | :--- |
| **Source Delivery Rows** | `200,999` | Raw baseline delivery records |
| **Processed Delivery Rows** | `200,999` | **100% Exact Match (0 added/dropped)** |
| **Exact Duplicate Rows** | `0` | **0 Duplicates** |
| **Contested Matches** | `867` | Matches with delivery telemetry (867 / 883) |
| **Contested Innings** | `1,724` | 867 Inn 1 + 845 Inn 2 + 6 Inn 3 + 6 Inn 4 |
| **Super Over Matches** | `6` | 6 matches (38 Super Over deliveries) |
| **Chase Deliveries (Inn 2 & 4)** | `95,247` | Total chase deliveries in dataset |
| **Chase Deliveries with Valid RRR** | `95,247` | Active chase deliveries before target met |
| **Revised-Overs Matches (`is_overs_revised`)** | `34` | Matches with revised overs in matches.csv |
| **Revised-Target Matches (`is_target_revised`)** | `23` | Matches with DLS revised targets in matches.csv |
| **Shortened Matches (`is_shortened_match`)** | `34` | Matches where scheduled overs were reduced (< 120 balls) |
| **Abandoned / No-Result Matches** | `40` | Weather curtailments in matches.csv (0 balls) |
| **Validation Registry Checks Executed** | **`18`** | **18 / 18 Executable Checks Passed** |

---

## 2. Executable Validation Registry

| Check ID | Validation Scope | Execution Assertion | Status | Result Details |
| :---: | :--- | :--- | :---: | :--- |
| **V01** | Delivery row count preservation | Executable check | **PASS** | Count=200,999 |
| **V02** | Duplicate delivery identity | Executable check | **PASS** | Duplicates=0 |
| **V03** | Referential integrity (match_id) | Executable check | **PASS** | Orphan matches=0 |
| **V04** | Referential integrity (team_ids) | Executable check | **PASS** | Invalid teams=0 |
| **V05** | Referential integrity (player_ids) | Executable check | **PASS** | Invalid players=0 |
| **V06** | Cumulative runs reconciliation | Executable check | **PASS** | Innings mismatches=0 |
| **V07** | Cumulative wickets reconciliation | Executable check | **PASS** | Innings mismatches=0 |
| **V08** | Legal balls bowled reconciliation | Executable check | **PASS** | Innings mismatches=0 |
| **V09** | Scheduled balls invariant (> 0) | Executable check | **PASS** | Non-positive scheduled=0 |
| **V10** | Balls remaining non-negativity | Executable check | **PASS** | Negative before=0, after=0 |
| **V11** | Wickets in hand non-negativity | Executable check | **PASS** | Negative before=0, after=0 |
| **V12** | Innings progress boundedness [0, 1] | Executable check | **PASS** | Out of bounds=0 |
| **V13** | Target runs constancy within innings | Executable check | **PASS** | Max distinct targets per inn=1 |
| **V14** | Runs required non-negativity | Executable check | **PASS** | Negative req before=0, after=0 |
| **V15** | First innings RRR isolation | Executable check | **PASS** | Non-null 1st inn RRR=0 |
| **V16** | Required run rate non-negativity | Executable check | **PASS** | Negative RRR=0 |
| **V17** | Super Over isolation | Executable check | **PASS** | Deliveries=38, scheduled=[6] |
| **V18** | No Cartesian row explosion | Executable check | **PASS** | Final count=200999 |

---

## 3. Data Leakage Protections

1. **Pre-Delivery vs Post-Delivery State**: Every delivery strictly distinguishes `_before` state (available when the bowler runs in and the batter prepares to strike) from `_after` state (resulting from the delivery event).
2. **Strict First-Innings Isolation**: First-innings deliveries are never assigned a synthetic target or required run rate. State variables reflect live cumulative progress (`runs_before`, `wickets_lost`, `balls_remaining`, `crr`).
3. **Explicit Post-Match Provenance**: Final match outcomes (`post_match_winner_team_id`, `post_match_result`, `post_margin_value`, `post_margin_type`, `post_innings_total_runs`) are prefixed with `post_` to ensure they are never ingested as live features.

---

## 4. Missing-Values Profile & Structural Classifications

| Column Name | Missing Count | Missing % | Missingness Category | Dataset-Grounded Explanation |
| :--- | :--- | :--- | :--- | :--- |
| `win_team_id` | 1,932 | 0.96% | `no-result/abandoned` | Matches ending in No Result (21), Abandoned (19), or Tied without super over (1). |
| `extras_type` | 189,167 | 94.11% | `event-dependent` | Legal deliveries without extras conceded. |
| `dismissal_type_raw` | 190,118 | 94.59% | `event-dependent` | Deliveries on which no wicket fell. |
| `dismissal_type_cleaned` | 190,118 | 94.59% | `event-dependent` | Deliveries on which no wicket fell. |
| `dismissed_player_id_raw` | 190,107 | 94.58% | `event-dependent` | Deliveries without dismissal (populated on 12 retired hurt balls; unpopulated on 1 retire out). |
| `dismissed_player_id_cleaned` | 190,106 | 94.58% | `event-dependent` | Deliveries without dismissal (imputed for Hardik Pandya's Retire Out). |
| `bowl_speed_cleaned` | 77,862 | 38.74% | `telemetry missing` | Unrecorded radar speed or failed validated physical bounds (<= 0 or > 165 km/h). |
| `stroke` | 6,158 | 3.06% | `telemetry missing` | Leaves, unoffered balls, wides without bat contact, or sensor classification gap. |
| `delivery_style` | 391 | 0.19% | `telemetry missing` | Unclassified bowler delivery movement. |
| `over_or_around` | 407 | 0.20% | `telemetry missing` | Missing bowling crease angle telemetry. |
| `current_run_rate_before` | 1,843 | 0.92% | `structurally undefined` | Innings opening delivery or before first legal delivery is completed (division by zero). |
| `current_run_rate_after` | 119 | 0.06% | `structurally undefined` | Deliveries where only illegal balls (wides/no-balls) have occurred so far (legal_balls_bowled = 0). |
| `target_runs` | 105,752 | 52.61% | `structurally undefined` | Innings 1 and Innings 3; setting target, no chase target exists. |
| `runs_required_before` | 105,752 | 52.61% | `structurally undefined` | Innings 1 and Innings 3; setting target. |
| `runs_required_after` | 105,752 | 52.61% | `structurally undefined` | Innings 1 and Innings 3; setting target. |
| `required_run_rate_before` | 105,752 | 52.61% | `structurally undefined` | Innings 1 & 3; plus chase deliveries after target already reached. |
| `required_run_rate_after` | 106,009 | 52.74% | `structurally undefined` | Innings 1 & 3; plus chase deliveries after final legal ball where balls_remaining_after = 0. |
| `rrr_crr_delta_before` | 106,647 | 53.06% | `structurally undefined` | Innings 1 & 3; plus first delivery of Innings 2 before CRR is established. |
| `post_match_winner_team_id` | 1,932 | 0.96% | `no-result/abandoned` | Matches without a recorded winning team. |
| `post_margin_value` | 4,061 | 2.02% | `match-state dependent` | Matches ending in No Result, Abandoned, or Super Over where margin is not denominated in runs/wickets. |

---

## 5. Unresolved Analytical Questions for Stage 3

1. **First-Innings Baseline Expectations**: First innings lacks an explicit required run rate. How should venue-adjusted, over-by-over expected final score be estimated objectively without arbitrary heuristics?
2. **Opposition & League Strength Weighting**: How should performance against Associate nations in regional qualifiers be mathematically calibrated against high-density elite fixtures like the IPL or India vs Australia encounters?
3. **Qualification & Sample-Size Criteria**: What minimum delivery thresholds under pressure should be required before ranking batters and bowlers to prevent small-sample variance from dominating?

---
*Report generated by PinkOps Pipeline | Operation Pink Panther*