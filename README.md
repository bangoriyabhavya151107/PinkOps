# Operation Pink Panther (PinkOps)

**Project**: Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand**: PinkOps  
**Objective**: Identify the most reliable batters and bowlers under pressure in T20 cricket using competition match data.  
**Working Slogan**: Zero Choke. All Smoke.  

> [!IMPORTANT]  
> **Progressive Engineering Discipline & Current Project State**:
> - **Stage 1 (Completed & Verified)**: Raw data discovery, structural validation, schema auditing, and anomaly cataloging.
> - **Stage 2 & 2.1 (Completed & Verified)**: Trusted match-state construction, cumulative innings tracking, chase dynamics, leakage prevention, and an 18-point automated validation registry.
> - **Stage 3 & 3.1 (Completed & Verified)**: Continuous pressure formulation, contextual expectation modeling, opposition strength adjustments, and exposure diagnostics.
> - **Stage 4.0 (Completed & Remediated)**: Reliability architecture, estimand freeze (Spec B), player attribution audit, and lower uncertainty bound derivation.
> - **Stage 4.1 (Completed & Verified)**: Multi-dimensional uncollapsed player evidence profiling across tactical roles and 6 reliability archetypes.
> - **Stage 4.1.1 (Completed, Hardened & Reconciled)**: Independent reproduction, mathematical derivation of uncertainty bounds, genuine 15-branch methodological multiverse recomputation, strengthened clutch CEM matching, end-to-end data leakage provenance audit, and a comprehensive 28-point automated test suite (T01–T28, 100% pass rate).
> - **Stage 5 (Completed & Verified)**: Candidate selection across 8 selection gates, tactical role portfolios, Final 10 Batters and Final 10 Bowlers, 20 analytical target dossiers, strategic auction board (MUST TARGET, TARGET, VALUE TARGET, BACKUP), and a 30-assertion automated test suite (T01–T30, 100% pass rate). Zero fabricated prices or single-score collapse.
> - **Stage 6 (Final Competition Delivery & Submission Package)**: Repository truth reconciliation, player evidence defense dossiers, master evidence ledger, competition strategy narrative, judge defense briefs, provenance mapping, and a 35-assertion final verification gate.

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
- `duckdb` (high-performance analytical queries)
- `scipy` (Empirical Bayes & rank statistics)
- `scikit-learn` (stratified cross-validation)
- `pypdf` (problem statement PDF validation)

---

## 3. Pipeline Execution (Stages 1 through 4.1.1)

The complete analytical pipeline is fully reproducible from the project root:

### Step 1: Data Discovery & Audit
```bash
python src/01_data_audit.py
```
- Profiling of all raw competition files.
- Generates [`outputs/data_audit_report.md`](file:///D:/PinkOps/outputs/data_audit_report.md).

### Step 2: Trusted Match-State Construction
```bash
python src/02_build_match_state.py
```
- Produces `data/processed/match_state.parquet` (200,999 delivery rows × 96 columns).
- Generates [`outputs/match_state_validation.md`](file:///D:/PinkOps/outputs/match_state_validation.md).

### Step 3: Pressure Discovery & Expected Outcome
```bash
python src/03_pressure_discovery.py
python src/stage_3_1/run_all.py
```
- Produces baseline models, WPLI validation, and exposure diagnostics.

### Step 4: Reliability Architecture & Spec Freeze
```bash
python src/stage_4_0/run_stage_4_0.py
```
- Freezes Specification B (excluding recent-12 self-conditioning).

### Step 5: Multi-Dimensional Evidence Profiling
```bash
python src/stage_4_1/stage_4_1_pipeline.py
```
- Produces `data/processed/stage_4_1_player_evidence.parquet` (1,535 players × 33 dimensions).
- Classifies players into 6 reliability archetypes without single-score collapse.

### Step 6: Stage 4.1.1 Hardening & Independent Validation
```bash
# Run population reconciliation
python src/stage_4_1_1/population_reconciliation.py

# Run delivery-level player attribution audit
python src/stage_4_1_1/attribution_audit.py

# Run Monte Carlo LUB simulation truth test (14,000 synthetic players)
python src/stage_4_1_1/lub_validation.py

# Run strengthened clutch coarsened exact matching
python src/stage_4_1_1/clutch_matching.py

# Run genuine methodological multiverse engine (15 specifications)
python src/stage_4_1_1/multiverse.py

# Run end-to-end data leakage provenance audit (31 pipeline features)
python src/stage_4_1_1/leakage_audit.py

# Execute the 28-point comprehensive automated test suite (T01 - T28)
python src/stage_4_1_1/test_stage_4_1_1.py
```

### Step 7: Stage 5 Squad Assembly & Final Player Selection
```bash
# Enrich player evidence with 75 contextual dimensions
python src/stage_5/build_stage_5_evidence.py

# Execute selection gates, candidate pools, and final 10+10 selections
python src/stage_5/candidate_selection.py

# Generate 20 in-depth analytical player target dossiers
python src/stage_5/generate_target_files.py

# Generate auction board and strategic mission brief
python src/stage_5/auction_strategy.py

# Execute the 30-point Stage 5 automated test suite (T01 - T30)
python src/stage_5/test_stage_5.py
```

### Step 8: Stage 6 Final Competition Delivery & Defense Package
```bash
# Execute Stage 6 evidence defense, provenance mapping, and submission compilation
python src/stage_6/build_stage_6_defense.py

# Execute the 35-point comprehensive Stage 6 verification suite (T01 - T35)
python src/stage_6/test_stage_6.py
```

---

## 4. Key Governance Invariants

1. **Strict Opportunity / Performance Separation:** Opportunity depends strictly on pre-delivery match state; performance is the residual outcome.
2. **Zero Single-Score Collapse:** Player reliability is fundamentally multi-dimensional; no scalar "PinkOps Score" is computed.
3. **Frequentist Lower Uncertainty Bound:** $\text{LUB}_{20} = \hat{\mu}_{\text{EB}} - 0.842 \cdot \text{SE}_{\text{EB}}$ acts as a conservative downside risk floor, penalizing small samples without distorting player ranks.
4. **Isolated Super Overs:** Super Over deliveries (38 balls across 6 matches) are isolated in a dedicated stress register and excluded from regular 20-over expectation models.
5. **Audited Selection & Zero Price Fabrication:** Final 10 Batters and Final 10 Bowlers are selected across 8 multidimensional gates. PinkOps strictly adheres to official competition rules and never fabricates artificial auction prices or purse limits.

---

*Operation Pink Panther — Built for Rajasthan Royals SupeRR Selector Season 2.*
