# PinkOps — Stage 4.0 Remediation: Canonical Delivery Population Reconciliation

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_population_reconciliation.md`  
**Stage:** 4.0 Remediation (Fix 5)  
**Governance Status:** RECONCILED & AUDITED  

---

## 1. Executive Summary & Purpose

In sports predictive modeling and competition-grade data science, statistical precision demands unambiguous population accounting. The Stage 4.0 audit flagged potential ambiguity between the total raw delivery universe and the normal-innings modeling dataset.

This document establishes the **authoritative population reconciliation** for Operation Pink Panther. Every model, baseline regression, and attribution engine downstream must strictly reference these reconciled numbers and adhere to the canonical terminology.

---

## 2. Canonical Population Accounting

### 2.1 The Exact Mathematical Reconciliation
The competition data contains:
- **Raw Delivery Universe:** Exactly **200,999** delivery rows.
- **Normal-Innings Modeling Universe:** Exactly **200,961** delivery rows.
- **Super Over Descriptive Universe:** Exactly **38** delivery rows.

$$\text{Raw Delivery Universe } (200,999) - \text{Super Over Universe } (38) = \text{Normal-Innings Modeling Universe } (200,961)$$

$$\text{Innings 1 } (105,727) + \text{Innings 2 } (95,234) = 200,961 \text{ deliveries}$$

$$\text{Innings 3 } (25) + \text{Innings 4 } (13) = 38 \text{ Super Over deliveries}$$

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                  RAW BALL-BY-BALL UNIVERSE: 200,999                    │
   │            (867 matches with valid delivery-level telemetry)           │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┴──────────────────────────────┐
        ▼                                                             ▼
   [ NORMAL-INNINGS MODELING ]                               [ SUPER OVER UNIVERSE ]
   Total Deliveries: 200,961                                 Total Deliveries: 38
   Innings 1: 105,727 balls                                  Innings 3: 25 balls
   Innings 2: 95,234 balls                                   Innings 4: 13 balls
   Matches: 867 contested                                    Matches: 6 tied matches
   Status: Primary Modeling Set                              Status: Isolated Stress-Test
```

---

## 3. Comprehensive Multi-Stage Reconciliation Table

The following table reconciles all datasets, models, and analytical subsets across Operation Pink Panther:

| Population / Subset Name | Source Artifact | Delivery Count | Match Count | Super Overs Included? | Modeling Status & Governance Role |
|---|---|---:|---:|:---:|---|
| **Raw Ball-by-Ball Universe** | `data/raw/.../ball_by_ball.csv` | **200,999** | 867 | Yes | **Immutable Raw Ground Truth.** Stored in immutable directory. |
| **Canonical Match State Parquet** | `data/processed/match_state.parquet` | **200,999** | 867 | Yes | **Full Validated Telemetry.** Preserves all original deliveries with 96 enriched features. |
| **Normal-Innings Modeling Universe** | `match_state.parquet` (Innings 1 & 2) | **200,961** | 867 | No | **Primary Modeling Universe.** Used for expectation baselines, VA attribution, and Stage 4.1 evidence. |
| **Super Over Descriptive Universe** | `match_state.parquet` (Innings 3 & 4) | **38** | 6 | Yes | **Isolated Qualitative Stress-Test.** Excluded from regular regressions due to extreme 48.0% wicket rate. |
| **Second-Innings Chase Deliveries** | `match_state.parquet` (Innings == 2) | **95,234** | 845 | No | **Chase Pressure Evaluation Subset.** All 2nd-innings deliveries across 845 contested run chases. |
| **Valid Required Run Rate Subset** | `match_state.parquet` (Innings == 2 & RRR != null) | **95,234** | 845 | No | **Active Chase Leverage Subset.** Deliveries with computable pre-delivery RRR and Target. |
| **Revised-Overs Matches Subset** | `match_state.parquet` (`is_overs_revised == true`) | **4,433** | 34 | No | **Rain/Shortened Match Context.** 34 matches with reduced scheduled overs (DLS / rain). |
| **Revised-Target Matches Subset** | `match_state.parquet` (`is_target_revised == true`) | **3,727** | 23 | No | **DLS / Target Revision Context.** 23 matches with revised numerical targets. |

---

## 4. Reconciling Across Project Stages

1. **Stage 1 (Data Discovery & Audit):** Audited all 200,999 rows in raw `ball_by_ball.csv`.
2. **Stage 2 & 2.1 (Match-State Construction & Hardening):** Validated all 200,999 delivery rows across 867 matches and 1,724 innings. Added flags `is_super_over` (38 deliveries), `is_overs_revised` (34 matches), and `is_target_revised` (23 matches).
3. **Stage 3 & 3.1 (Pressure Discovery & Modeling):** Evaluated expectation models strictly on the **200,961 normal-innings deliveries** (Innings 1 and 2), explicitly isolating the 38 Super Over deliveries.
4. **Stage 4.0 & 4.1 (Reliability Architecture & Selection Framework):** Adopts the **200,961 normal-innings universe** for all quantitative player execution, reliability, downside, consistency, and uncertainty computations. Super Over deliveries are recorded as qualitative context metadata in Layer 6 (`super_over_balls`).

---

## 5. Downstream Invariants & Reporting Rules

To eliminate reporting errors:
- **Rule 5.1:** Never describe 200,961 as the "total raw delivery count." The total raw delivery count is **200,999**.
- **Rule 5.2:** Never describe 200,999 as the "model training sample size." The normal-innings modeling population is **200,961**.
- **Rule 5.3:** Super Over deliveries (38 balls) must remain strictly quarantined from normal expectation curve fitting.

*Document Approved by PinkOps Quantitative Governance Committee.*
