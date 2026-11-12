# Operation Pink Panther (PinkOps)

**Project**: Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand**: PinkOps  
**Objective**: Identify the most reliable batters and bowlers under pressure in T20 cricket using competition match data.  

> [!IMPORTANT]  
> **Progressive Engineering Discipline**:
> - **Stage 1 (Completed)**: Raw data discovery, structural validation, schema auditing, and anomaly cataloging.
> - **Stage 2 & 2.1 (Completed)**: Trusted match-state construction, semantic hardening, cumulative innings tracking, chase dynamics, leakage prevention, and an 18-point automated validation registry.
> - **Strict Competition Constraints**: In accordance with project instructions, **no pressure engine, no pressure weights, no arbitrary thresholds, and no player rankings** have been introduced.

---

## 1. Data Repository & Immutability Rules

All raw competition data packs provided for the competition belong in:

```
data/raw/
```

- **IMMUTABILITY MANDATE**: Raw files inside `data/raw/` must **NEVER** be modified, overwritten, or renamed.
- All cleaning, schema standardization, and feature enrichment pipelines treat `data/raw/` as read-only and write intermediate outputs to `data/processed/` or artifacts to `outputs/`.
- Expected source files inside `data/raw/`:
  - `competitions.csv`
  - `teams.csv`
  - `matches.csv`
  - `ball_by_ball.csv`
  - `competition_team_player_mapping.csv`
  - `playing_eleven.csv`
  - `Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`

---

## 2. Environment Setup

### Prerequisites
- Python 3.10+ (Python 3.13 tested)
- pip package manager

### 1. Create Virtual Environment
From the project root:

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Core dependencies:
- `pandas` (tabular analysis)
- `numpy` (vectorized operations)
- `pyarrow` (high-performance columnar parquet storage)
- `pypdf` (problem statement PDF validation)
- `duckdb` (high-performance analytical queries)

---

## 3. Pipeline Execution

The entire pipeline is fully reproducible from the project root:

### Step 1: Data Discovery & Audit
```bash
python src/01_data_audit.py
```
- Inspects, profiles, and validates every raw file.
- Tests primary key uniqueness and foreign key referential integrity.
- Generates [`outputs/data_audit_report.md`](file:///D:/PinkOps/outputs/data_audit_report.md).

### Step 2: Trusted Match-State Construction & Hardening
```bash
python src/02_build_match_state.py
```
- Loads raw delivery and match files without altering raw data.
- Handles known Stage 1 anomalies (retired hurt, retire out, player name collisions, speed glitches).
- Derives cumulative match state, legal delivery counters, and chase dynamics.
- Enforces strict leakage prevention rules.
- Executes an **18-point Validation Registry** where every reported check is an executable assertion.
- Produces:
  - `data/processed/match_state.parquet` (200,999 delivery rows × 96 columns)
  - [`outputs/match_state_validation.md`](file:///D:/PinkOps/outputs/match_state_validation.md) (Automated validation report with column-specific missingness taxonomy)
  - [`outputs/match_state_sample.csv`](file:///D:/PinkOps/outputs/match_state_sample.csv) (79 data-driven representative rows for manual review)
  - [`outputs/legal_delivery_audit.md`](file:///D:/PinkOps/outputs/legal_delivery_audit.md) (Empirical audit of extras and legal delivery classification)
  - [`outputs/super_over_validation.md`](file:///D:/PinkOps/outputs/super_over_validation.md) (Independent audit of all 6 Super Over contests)
  - [`outputs/stage_2_1_hardening_report.md`](file:///D:/PinkOps/outputs/stage_2_1_hardening_report.md) (Comprehensive hardening pass summary & PASS decision)

### Step 3: Pressure Discovery & Expected-Outcome Engine
```bash
python src/03_pressure_discovery.py
```
- Audits continuous pressure candidate variables (14 dimensions profiled).
- Computes pre-match dynamic Elo ratings across all 867 matches with strict causal ordering.
- Calculates venue and competition scoring baselines with Empirical Bayes shrinkage.
- Trains and validates First-Innings Expected Runs and Chase Win Probability models across Match-Grouped, Temporal, and LOCO holdouts.
- Profiles player opportunity distributions under pressure across 888 batters and 647 bowlers.
- Enforces active assertion gates confirming zero leakage.
- Produces:
  - `data/processed/pressure_variable_stats.csv`
  - `data/processed/venue_baselines.csv`
  - `data/processed/competition_baselines.csv`
  - `data/processed/team_pre_match_elo.csv`
  - `data/processed/model_validation_metrics.csv`
  - `data/processed/player_opportunity_profiles.parquet`
  - [`outputs/stage_3_methodology_design.md`](file:///D:/PinkOps/outputs/stage_3_methodology_design.md)
  - [`outputs/pressure_variable_audit.md`](file:///D:/PinkOps/outputs/pressure_variable_audit.md)
  - [`outputs/opposition_strength_design.md`](file:///D:/PinkOps/outputs/opposition_strength_design.md)
  - [`outputs/stage_3_leakage_audit.md`](file:///D:/PinkOps/outputs/stage_3_leakage_audit.md)
  - [`outputs/stage_3_validation_plan.md`](file:///D:/PinkOps/outputs/stage_3_validation_plan.md)

---

## 4. Stage 2.1 Engineering Details

### What Was Derived
1. **Cumulative Delivery State**:
   - `runs_before`, `runs_on_delivery`, `runs_after`
   - `wickets_before`, `wickets_on_delivery`, `wickets_after`
   - `balls_before` (legal deliveries bowled before), `legal_balls_bowled` (cumulative legal balls including current ball)
   - `balls_remaining_before`, `balls_remaining_after` (bounded `[0, 120]` for T20, `[0, 6]` for Super Overs)
   - `wickets_in_hand_before`, `wickets_in_hand_after` (bounded `[0, 10]` for standard, `[0, 2]` for Super Overs)
   - `innings_progress_before`, `innings_progress_after` (bounded `[0.0, 1.0]`)
   - `current_run_rate_before`, `current_run_rate_after`
2. **Chase Context (Innings 2 & 4)**:
   - `target_runs` (incorporating actual DLS revised targets where applicable)
   - `runs_required_before`, `runs_required_after` (bounded `>= 0`)
   - `required_run_rate_before`, `required_run_rate_after` (strictly null for 1st innings)
   - `rrr_crr_delta_before`
3. **Innings Scope (Explicitly Separated)**:
   - `is_super_over`: True strictly for Innings 3 & 4.
   - `is_overs_revised`: True if overs allocation was revised.
   - `is_target_revised`: True if a DLS revised target was applied.
   - `is_shortened_match`: True only when scheduled legal balls are reduced (< 120).
4. **Post-Match Context (Leakage Protected & Parsed)**:
   - `post_innings_total_runs`, `post_innings_total_wickets`, `post_innings_total_legal_balls`
   - `post_innings_overs_formatted`, `post_innings_ended_normally`
   - `post_match_winner_team_id`, `post_match_result` (raw string)
   - `post_margin_value` (numeric), `post_margin_type` ('runs', 'wickets', 'super_over', 'tie', 'none')
   - `post_match_is_tie`, `post_match_had_super_over`

### What Was Intentionally NOT Derived
- **No Pressure Scores**: No subjective thresholds, weights, or pressure indices.
- **No Player Rankings**: No Top 10 lists, no batter or bowler evaluations.
- **No Clutch / PVA / Win Expectancy Scores**: Reserved for Stage 3 after objective pressure definitions are formulated.
- **No Fake First-Innings Targets**: First innings is strictly preserved without fabricating synthetic required run rates.

### Data Leakage Protections
- **Pre-Delivery vs Post-Delivery Horizon**: Every delivery strictly distinguishes `_before` state (available when the batter takes guard) from `_after` state (resulting from the delivery event).
- **Post-Match Provenance Tagging**: All terminal match variables are explicitly prefixed with `post_` so downstream models cannot ingest future outcome data.

### Anomaly Handling Rules
- **Player Identity**: Joined strictly on `player_id`. `player_name` is treated as display-only to prevent collapsing the 7 distinct athlete name collisions.
- **Retired Hurt**: 12 deliveries with `is_wicket=False` and `dismissed_player_id` populated are flagged as `is_retired_hurt=1`. Bowler is awarded 0 wickets (`is_bowler_wicket=0`).
- **Retire Out**: Hardik Pandya's unpopulated `dismissed_player_id` on ball 127899 is resolved to `striker_id` (`4220`).
- **Radar Speed**: Preserved `bowl_speed_raw`; created `bowl_speed_cleaned` correcting decimal shift glitches (`1456.1` &rarr; `145.61 km/h`).
- **Spelling**: Normalized `Obstracting the field` to `Obstructing the field`.
- **Lineup Duplicates**: `playing_eleven` deduplicated by `(match_id, player_id)` taking minimum batting order.

---

## 5. Summary Metrics

| Stage 2.1 Metric | Verified Count / Status | Notes |
| :--- | :---: | :--- |
| **Output Delivery Rows** | `200,999` | 100% exact match with raw `ball_by_ball.csv` |
| **Matches Contested** | `867` | All 16 unplayed/abandoned matches isolated |
| **Innings Contested** | `1,724` | 867 Inn 1 + 845 Inn 2 + 6 Inn 3 + 6 Inn 4 |
| **Super Over Contests** | `6` matches | 38 balls across 6 tied matches |
| **Chase Deliveries with Valid RRR** | `95,247` | Innings 2 & 4 deliveries before target reached |
| **Revised-Overs Matches** | `34` | Matches with revised overs in matches.csv |
| **Revised-Target Matches** | `23` | Matches with DLS revised targets in matches.csv |
| **Shortened Matches** | `34` | Matches where scheduled overs were reduced (< 120 balls) |
| **Abandoned / No-Result Matches** | `40` | Weather curtailments in matches.csv (0 balls) |
| **Validation Checks Executed** | `18` | All 18 checks executed via assertions |
| **Validation Failures** | `0` | 18 / 18 PASS |
| **Stage 2.1 Decision** | **PASS** | Approved for Stage 3 |

---

## 6. Repository Structure

```
PinkOps/
├── data/
│   ├── raw/                                    # Read-only competition files (never modified)
│   └── processed/
│       ├── match_state.parquet                 # Canonical delivery-level match-state table (200,999 rows)
│       ├── pressure_variable_stats.csv         # Continuous pressure variables empirical profile
│       ├── venue_baselines.csv                 # 97 venues with Empirical Bayes shrinkage baselines
│       ├── competition_baselines.csv           # 138 competition scoring baselines
│       ├── team_pre_match_elo.csv              # Dynamic pre-match Elo ratings (867 matches)
│       ├── model_validation_metrics.csv        # Multi-scheme holdout validation benchmark
│       └── player_opportunity_profiles.parquet # Opportunity volume across 888 batters & 647 bowlers
├── outputs/
│   ├── data_audit_report.md                    # Stage 1: 14-section data audit report
│   ├── match_state_validation.md               # Stage 2.1: 18-point automated validation report
│   ├── match_state_sample.csv                  # Stage 2.1: 79 data-driven representative rows
│   ├── legal_delivery_audit.md                 # Stage 2.1: Legal delivery empirical audit
│   ├── super_over_validation.md                # Stage 2.1: Super Over independent audit
│   ├── stage_2_1_hardening_report.md           # Stage 2.1: Hardening report & PASS verdict
│   ├── stage_3_methodology_design.md           # Stage 3.0: 20-section architectural methodology design
│   ├── pressure_variable_audit.md              # Stage 3.0: 14 continuous pressure variables audit
│   ├── opposition_strength_design.md           # Stage 3.0: Dynamic Elo & opponent attack design
│   ├── stage_3_leakage_audit.md                # Stage 3.0: Forensic causal timeline leakage audit
│   └── stage_3_validation_plan.md              # Stage 3.0: Match-grouped, temporal & LOCO validation
├── src/
│   ├── 01_data_audit.py                        # Stage 1 data audit execution script
│   ├── 02_build_match_state.py                 # Stage 2.1 match-state pipeline script
│   └── 03_pressure_discovery.py                # Stage 3.0 pressure discovery & validation script
├── requirements.txt                            # Pinned python project dependencies
└── README.md                                   # Comprehensive project documentation
```
