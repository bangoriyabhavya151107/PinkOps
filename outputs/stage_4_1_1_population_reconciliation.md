# PinkOps — Stage 4.1.1: Canonical Population Reconciliation & Delivery Accounting Report
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Verification Script:** `src/stage_4_1_1/population_reconciliation.py`  
**Dataset Artifact:** [`data/processed/stage_4_1_1_population_reconciliation.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_population_reconciliation.csv)  
**Date:** November 2026  

---

## 1. Executive Summary: Denominator Integrity

A foundational requirement of statistical modeling is maintaining absolute transparency over sample denominators. Changing sample filters mid-pipeline without formal accounting creates reconciliation drift.

This report documents the **exact delivery reconciliation between the raw competition data and downstream analytical subsets**.

---

## 2. Canonical Reconciliation Ledger

The delivery universe decomposes into two distinct, mutually exclusive populations:

$$N_{\text{raw}} = N_{\text{normal}} + N_{\text{super\_over}}$$

$$200,999 = 200,961 + 38$$

### Complete Population Breakdown
| Population Segment | Delivery Count | Percentage of Raw | Unique Matches | Innings Covered | Methodological Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Raw Competition Telemetry** | **200,999** | **100.00%** | **867** | 1, 2, 3, 4 | Immutable source baseline in [`data/raw/`](file:///D:/PinkOps/data/raw/). |
| **Super Over Deliveries** | **38** | **0.019%** | **6** | 3, 4 | **Isolated.** Excluded from regular expectation models due to extreme sample sparsity. |
| — Innings 3 (First Super Over) | 25 | 0.012% | 6 | 3 | Isolated stress register. |
| — Innings 4 (Second Super Over) | 13 | 0.006% | 6 | 4 | Isolated stress register. |
| **Normal-Innings Modeling Universe** | **200,961** | **99.981%** | **867** | 1, 2 | **Frozen Canonical Modeling Universe.** Used for all expectation and attribution models. |
| — First Innings (Defending) | 105,727 | 52.601% | 867 | 1 | Target setting phase. |
| — Second Innings (Chasing) | 95,234 | 47.380% | 867 | 2 | Target chase phase with valid Required Run Rate (RRR). |

---

## 3. Super Over Policy & Audit Register

Super Overs occur in **6 matches** and generate **38 total deliveries**:
- **Why Super Overs are isolated:** A Super Over consists of a 6-ball maximum shootout with 2 wickets in hand. The resource dynamics, tactical risk tolerance, and run-expectancy curves differ radically from standard 20-over cricket. Pooling 38 Super Over balls into a 200,000-ball regression model either distorts the standard baseline or subjects those 38 deliveries to inappropriate 20-over expectations.
- **Audit Register:** The 38 Super Over deliveries are preserved in `match_state.parquet` with `is_super_over = 1` for qualitative review and descriptive stress-testing, but are strictly excluded from the baseline player expectation and shrinkage models.

---

*End of Stage 4.1.1 Population Reconciliation Report.*
