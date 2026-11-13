# PinkOps — Stage 4.1.1: Comprehensive Pipeline Reproducibility Report
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Date:** November 2026  
**Status:** 100% Deterministic & End-to-End Auditable  

---

## 1. Execution Environment & Dependencies

The complete analytical pipeline was verified from a clean virtual environment:

- **Operating System:** Windows 11 Enterprise (x86_64)
- **Python Runtime:** Python 3.13.0
- **Virtual Environment Path:** `D:\PinkOps\.venv`
- **Shell / Terminal:** PowerShell 7+

### Frozen Dependencies (`requirements.txt`)
```text
pandas>=2.0.0      # Tested: 2.2.3 (Tabular transformations & indexing)
numpy>=1.24.0      # Tested: 2.1.2 (Vectorized math & array operations)
duckdb>=1.0.0      # Tested: 1.1.3 (High-performance SQL queries over Parquet)
pyarrow>=15.0.0    # Tested: 18.0.0 (Columnar Parquet serialization)
scipy>=1.12.0      # Tested: 1.14.1 (Empirical Bayes & Spearman rank statistics)
scikit-learn>=1.4.0# Tested: 1.5.2 (Stratified splitting & baseline metrics)
pypdf>=4.0.0       # Tested: 5.1.0 (Problem statement PDF extraction)
```

---

## 2. Input Data Lineage & Immutability Ledger

Raw competition data located in [`data/raw/`](file:///D:/PinkOps/data/raw/) remains strictly read-only and immutable. No script in the repository modifies, writes to, or deletes any file in `data/raw/`.

| Raw File Name | File Size | Row Count | Primary Key / Index | Referential Integrity |
| :--- | :---: | :---: | :--- | :--- |
| `ball_by_ball.csv` | ~45.2 MB | 200,999 | `(match_id, innings, innings_ball_num)` | Links to `matches.csv` via `match_id` |
| `matches.csv` | ~185 KB | 867 | `match_id` | Links to `competitions.csv` via `comp_id` |
| `teams.csv` | ~12 KB | 114 | `team_id` | Referenced by home/away teams |
| `competitions.csv` | ~2.5 KB | 28 | `comp_id` | T20 leagues (IPL, BBL, PSL, CPL, etc.) |
| `playing_eleven.csv` | ~1.4 MB | 19,074 | `(match_id, team_id, player_id)` | Player match appearance registry |
| `competition_team_player_mapping.csv` | ~480 KB | 7,812 | `(comp_id, team_id, player_id)` | Squad membership roster |

---

## 3. End-to-End Pipeline Execution Order

To reproduce all project artifacts from scratch:

```bash
# 1. Activate Environment
.\.venv\Scripts\activate

# 2. Stage 1: Data Audit & Schema Profiling
python src/01_data_audit.py

# 3. Stage 2 & 2.1: Trusted Match-State Construction & Hardening
python src/02_build_match_state.py

# 4. Stage 3: Pressure Discovery & Expectation Engine Scaffolding
python src/03_pressure_discovery.py

# 5. Stage 3.1: WPLI Validation, Leakage Governance & Stability
python src/stage_3_1/run_all.py

# 6. Stage 4.0: Reliability Architecture & Spec Freeze
python src/stage_4_0/run_stage_4_0.py

# 7. Stage 4.1: Multi-Dimensional Player Evidence & Profile Classification
python src/stage_4_1/stage_4_1_pipeline.py

# 8. Stage 4.1.1 Hardening Passes:
# 8a. Reconcile Canonical Population
python src/stage_4_1_1/population_reconciliation.py

# 8b. Reconcile Player Attribution
python src/stage_4_1_1/attribution_audit.py

# 8c. Validate Lower Uncertainty Bound against Simulation Truth
python src/stage_4_1_1/lub_validation.py

# 8d. Strengthened Clutch Coarsened Exact Matching
python src/stage_4_1_1/clutch_matching.py

# 8e. Genuine Methodological Multiverse Engine
python src/stage_4_1_1/multiverse.py

# 9. Automated Executable Test Harness (22/22 Assertions)
python src/stage_4_1_1/test_stage_4_1_1.py
```

---

## 4. Deterministic Seeding & Random Operations

To guarantee 100% numerical determinism across runs:
- **Simulation Truth Seed:** `seed = 42` is fixed in `src/stage_4_1_1/lub_validation.py`.
- **All Sorting & Grouping:** Explicit secondary sort keys (e.g., `sort_values(['role', 'evidence_tier', 'lub_20'], ascending=[True, True, False])`) are enforced to prevent non-deterministic index ordering across platforms.

---

## 5. Machine-Readable Processed Artifacts Summary

| Artifact Path | Format | Row Count | Primary Purpose |
| :--- | :---: | :---: | :--- |
| [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) | Parquet | 200,999 | Canonical delivery telemetry with cumulative state |
| [`data/processed/stage_4_1_player_evidence.parquet`](file:///D:/PinkOps/data/processed/stage_4_1_player_evidence.parquet) | Parquet | 1,535 | 33-dimensional uncollapsed evidence table |
| [`data/processed/stage_4_1_player_classifications.csv`](file:///D:/PinkOps/data/processed/stage_4_1_player_classifications.csv) | CSV | 1,535 | Player reliability profile classifications |
| [`data/processed/stage_4_1_1_multiverse_results.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_multiverse_results.csv) | CSV | 15 | 15 independent methodological branches |
| [`data/processed/stage_4_1_1_lub_coverage.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_lub_coverage.csv) | CSV | 7 | Monte Carlo simulation truth recovery stats |
| [`data/processed/stage_4_1_1_clutch_balance.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_clutch_balance.csv) | CSV | 6 | Covariate balance (SMD) before and after CEM |
| [`data/processed/stage_4_1_1_attribution_audit.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_attribution_audit.csv) | CSV | 16 | Complete extra and dismissal ledger reconciliation |
| [`data/processed/stage_4_1_1_population_reconciliation.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_population_reconciliation.csv) | CSV | 9 | Delivery and match denominator reconciliation |
| [`data/processed/stage_4_1_1_governance_spec.json`](file:///D:/PinkOps/data/processed/stage_4_1_1_governance_spec.json) | JSON | — | Machine-readable single source of governance thresholds |

---

*End of Stage 4.1.1 Pipeline Reproducibility Report.*
