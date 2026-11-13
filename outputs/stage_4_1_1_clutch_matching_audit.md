# PinkOps — Stage 4.1.1: Strengthened Clutch Matching & Covariate Balance Audit
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Verification Script:** `src/stage_4_1_1/clutch_matching.py`  
**Dataset Artifact:** [`data/processed/stage_4_1_1_clutch_balance.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_clutch_balance.csv)  
**Date:** November 2026  

---

## 1. Executive Summary & Causal Discipline

A critical methodological trap in sports analytics is interpreting "clutch" (elevated performance under high pressure) as an innate causal power without adjusting for game situation. High-pressure balls disproportionately occur in death overs, when batting orders are deep, and when bowlers face aggressive swings. A batter who scores 14 runs in a death over under pressure is not automatically "more clutch" than when they score 6 runs in the powerplay; the phase and field restrictions are completely different.

To evaluate clutch performance with scientific integrity, we implement **multi-dimensional Coarsened Exact Matching (CEM)** that contrasts high-pressure deliveries against comparable low-pressure deliveries sharing the exact same pre-delivery game context.

> [!IMPORTANT]
> **GOVERNANCE RULING: NON-CAUSAL OBSERVATIONAL CONTRAST**  
> Even with strengthened CEM, the clutch metric ($\Delta_{\text{RVA}} = \text{RVA}_{\text{pressure}} - \text{RVA}_{\text{low\_pressure}}$) remains an **observational contrast**, not an individual causal treatment effect. We observe each delivery in only one potential state. This metric is retained as descriptive contextual evidence, not as a standalone ranking metric.

---

## 2. Multi-Dimensional Pre-Delivery Matching Design

Matching is performed exclusively on **pre-delivery covariates** across the 200,961 normal-innings deliveries:

1. **Innings Phase:** Powerplay (overs 1–6), Middle (overs 7–15), Death (overs 16–20).
2. **Wickets in Hand:** Low (1–3 wickets), Mid (4–6 wickets), High (7–10 wickets).
3. **Balls Remaining:** 1–30 balls, 31–60 balls, 61–90 balls, 91–120 balls.
4. **Required Run Rate / Rate Stress:** Sub-7.0, 7.0–9.5, 9.5–12.0, Over-12.0 rpo.
5. **Batting Order Tier:** Top (1–3), Middle (4–6), Lower (7–11).
6. **Bowling Style:** Pace vs. Spin.
7. **Opponent Pre-Match Elo:** Upper (>1530), Mid (1470–1530), Lower (<1470).
8. **Venue Scoring Baseline:** Low, Mid, High scoring environments.
9. **Chase Status:** 1st Innings Defend vs. 2nd Innings Chase.

This partitioning produces **2,069 multi-dimensional pre-delivery strata**.

---

## 3. Matched Common Support & Sample Size

- **High Pressure Deliveries (Treated):** 70,773 total deliveries; **24,279 retained in common support** (34.3%).
- **Low Pressure Deliveries (Control):** 130,188 total deliveries; **31,878 retained in common support** (24.5%).
- **Total Matched Cohort:** **56,157 deliveries**.
- **Effective Sample Size (ESS) after CEM weighting:** **7,588.3 deliveries**.

---

## 4. Covariate Balance Ledger (Before vs. After Matching)

The table below records the standardized mean differences (SMD) before and after matching:

| Covariate | Mean Treated (Unadj) | Mean Control (Unadj) | Raw SMD | Mean Treated (Matched) | Mean Control (Matched) | Matched SMD | SMD Reduction | Balance Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Pace Bowling Delivery Indicator** | 0.618 | 0.615 | +0.0069 | 0.626 | 0.626 | **0.0000** | **100.00%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Required Run Rate / Rate Urgency** | 10.567 | 8.297 | +0.6165 | 8.235 | 8.301 | **-0.0179** | **97.09%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Opponent Pre-Match Elo** | 1510.1 | 1509.0 | +0.0163 | 1509.3 | 1508.4 | **+0.0137** | **15.98%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Batting Order Position** | 5.639 | 2.907 | +1.3681 | 4.787 | 4.529 | **+0.1294** | **90.54%** | **Substantially Attenuated** |
| **Wickets in Hand** | 5.392 | 8.363 | -1.6659 | 6.220 | 6.957 | **-0.4133** | **75.19%** | **Substantially Attenuated** |
| **Balls Remaining** | 33.217 | 78.064 | -1.7666 | 34.746 | 46.175 | **-0.4502** | **74.51%** | **Substantially Attenuated** |

### Key Diagnostic Observations
1. **Elimination of Match-Up & Rate Imbalances:** Bowling style (Pace vs Spin), Required Run Rate, and Opponent Strength achieve near-zero post-matching SMDs ($|\text{SMD}| \le 0.018$).
2. **Massive Attenuation of Resource Disparities:** The immense structural imbalance between pressure and non-pressure deliveries (e.g., raw SMD of -1.77 in balls remaining and -1.67 in wickets in hand) is attenuated by **74.5% to 75.2%**.
3. **Residual Structural Gap:** Because high-pressure situations intrinsically concentrate in late overs with fewer wickets, exact balance across all resource dimensions cannot be achieved without discarding almost all death overs. The residual SMD of ~0.41 reflects the physical reality of T20 cricket, which is documented here as an explicit methodological diagnostic rather than swept under the rug.

---

*End of Stage 4.1.1 Clutch Matching Audit Report.*
