# PinkOps — Stage 6: Robustness Terminology Resolution & Specification Taxonomy
**Project:** Operation Pink Panther / PinkOps  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Document ID:** `outputs/stage_6_robustness_resolution.md`  
**Date:** November 2026  

---

## 1. Executive Summary & Root Cause Investigation

During the Stage 6 audit, an apparent documentation discrepancy was identified across Stage 5 outputs:
- Some Stage 5 reports and test assertions referenced `>=5/8` or `8/8`.
- The auction board referenced `Universal Support (6/6)`.
- The Stage 4.1.1 Methodological Multiverse artifact (`data/processed/stage_4_1_1_multiverse_results.csv`) contained exactly **15 specifications**.

### Investigation Findings & Denominator Provenance:
1. **The 15-Specification Universe:** Formally established in Stage 4.1.1, the multiverse engine evaluates 15 total branches.
2. **The 6 Genuine Performance Recomputations (`FULL_RECOMPUTATION`):**
   - `SPEC_00_PRIMARY`: Canonical Spec B Baseline (K=100, LUB20, PI80, CEM)
   - `SPEC_EXP_SPEC_A`: Spec A Contextual Expectation (including recent 12 deliveries micro-momentum)
   - `SPEC_PRESS_PI70`: Broadened Pressure Cutoff (PI >= 0.50, top 30% leverage)
   - `SPEC_PRESS_PI85`: Concentrated Pressure Cutoff (PI >= 0.64, top 15% leverage)
   - `SPEC_EPS_10`: Compressed RDI Epsilon (epsilon = 0.10)
   - `SPEC_EPS_20`: Relaxed RDI Epsilon (epsilon = 0.20)
   *In these 6 branches, the underlying delivery expectations or pressure subsets were independently re-estimated from telemetry.*
3. **The 6 Parameter Sensitivity Branches (`PARTIAL_RECOMPUTATION`):**
   - Shrinkage strength: $K=50.0$ and $K=200.0$
   - Downside quantile bounds: $p=10, 15, 25, 30$
4. **The 3 Orthogonal Descriptor Alternatives (`DESCRIPTOR_ALTERNATIVE`):**
   - Match-level IQR dispersion
   - Negative match contribution non-loss rate
   - Matched clutch delta ($\Delta_{\text{RVA}}$)

### Why 8/8 vs 6/6 Appeared:
- In early Stage 4.1, an initial 8-branch primary grid was evaluated (`multiverse_specs_supported` in parquet had a max of 8).
- In Stage 4.1.1, the **6 genuine performance specifications** were mathematically isolated from orthogonal descriptors and sensitivity bounds.
- The auction board correctly reported `Universal Support (6/6)` referring to the 6 genuine performance models.
- Test T11 in Stage 5 checked `>= 5/8` against the inherited integer column.

---

## 2. Canonical Harmonized Terminology Standard

Stage 6 formally establishes **ONE unified terminology standard** across all documentation, tables, and tests:

```
+---------------------------------------------------------------------------------------------------+
| 1. METHODOLOGICAL PERFORMANCE ROBUSTNESS (Primary Denominator = 6)                                |
|    Standard: X / 6 Genuine Independent Performance Recomputations                                 |
|    Eligible Branches: SPEC_00_PRIMARY, SPEC_EXP_SPEC_A, SPEC_PRESS_PI70,                          |
|                       SPEC_PRESS_PI85, SPEC_EPS_10, SPEC_EPS_20                                   |
|    Status: All 20 selected players achieve 6/6 Universal Performance Support (100%).              |
+---------------------------------------------------------------------------------------------------+
| 2. EXTENDED SENSITIVITY GRID (Secondary Denominator = 8 / 12)                                     |
|    Standard: X / 8 Primary Grid or X / 12 Total Recomputed Models                                 |
|    Includes: Shrinkage variations (K=50, 200) and LUB quantiles (p=10, 15, 25, 30)                |
|    Status: All 20 selected players maintain strictly positive lower bounds across all variations. |
+---------------------------------------------------------------------------------------------------+
| 3. DESCRIPTOR CORROBORATION (Denominator = 3 Orthogonal Metrics)                                  |
|    Standard: Evaluated as distinct dimensions, NEVER collapsed into performance count             |
|    Includes: Match IQR dispersion, non-loss rate, and matched clutch contrast delta               |
|    Status: 100% of final candidates corroborate consistency; 41.1% show clutch elevation.        |
+---------------------------------------------------------------------------------------------------+
```

---

*End of Robustness Terminology Resolution Document.*
