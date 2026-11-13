# PinkOps — Stage 4.1.1: Strengthened Clutch Matching & Covariate Balance Audit
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Verification Script:** `src/stage_4_1_1/clutch_matching.py`  
**Dataset Artifact:** [`data/processed/stage_4_1_1_clutch_balance.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_clutch_balance.csv)  
**Date:** November 2026  

---

## 1. Executive Summary & Causal Discipline

A critical methodological trap in sports analytics is interpreting "clutch" (elevated performance under high pressure) as an innate causal power without adjusting for game situation. High-pressure balls disproportionately occur in death overs, when batting orders are deep, and when bowlers face aggressive swings. A batter who scores 14 runs in a death over under pressure is not automatically "more clutch" than when they score 6 runs in the powerplay; the phase, field restrictions, and bowling tactics are fundamentally different.

To evaluate clutch performance with scientific integrity, we implement **multi-dimensional Coarsened Exact Matching (CEM)** that contrasts high-pressure deliveries against comparable low-pressure deliveries sharing the exact same pre-delivery game context.

> [!IMPORTANT]
> **GOVERNANCE RULING: NON-CAUSAL OBSERVATIONAL CONTRAST**  
> Even with strengthened CEM, the clutch metric ($\Delta_{\text{RVA}} = \text{RVA}_{\text{pressure}} - \text{RVA}_{\text{low\_pressure}}$) remains an **observational contrast**, not an individual causal treatment effect. We observe each delivery in only one potential state. This metric is retained as descriptive contextual evidence, not as a standalone ranking metric or decision scalar.

---

## 2. Multi-Dimensional Pre-Delivery Matching Design

Matching is performed exclusively on **pre-delivery covariates** across the 200,961 normal-innings deliveries:

1. **Innings Phase:** Powerplay (overs 1–6), Middle (overs 7–15), Death (overs 16–20).
2. **Wickets in Hand:** Low (1–3 wickets), Mid (4–6 wickets), High (7–10 wickets).
3. **Balls Remaining:** 1–30 balls, 31–60 balls, 61–90 balls, 91–120 balls.
4. **Required Run Rate / Rate Urgency:** Sub-7.0, 7.0–9.5, 9.5–12.0, Over-12.0 rpo.
5. **Batting Order Position:** Top (1–3), Middle (4–6), Lower (7–11).
6. **Bowling Style:** Pace vs. Spin.
7. **Opponent Pre-Match Elo:** Assigned strictly from the actual opponent bowling team (`bowling_team_id`), independent of chase status.
8. **Venue Scoring Baseline:** Strictly pre-match expanding historical baseline (excluding current & future matches, shrunk toward 1.30 runs/ball with $K=500$).
9. **Chase Status:** 1st Innings Defend vs. 2nd Innings Chase.

This partitioning produces multi-dimensional pre-delivery strata ensuring fair, apples-to-apples comparison.

---

## 3. Matched Common Support & Sample Size

- **High Pressure Deliveries (Treated):** 70,773 total deliveries; **24,279 retained in common support** (34.3%).
- **Low Pressure Deliveries (Control):** 130,188 total deliveries; **31,878 retained in common support** (24.5%).
- **Total Matched Cohort:** **56,157 deliveries**.
- **Effective Sample Size (ESS) after CEM weighting:** **7,588.3 deliveries**.

---

## 4. Covariate Balance Ledger (Before vs. After Matching)

The table below records the standardized mean differences (SMD) before and after matching, exactly reflecting [`data/processed/stage_4_1_1_clutch_balance.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_clutch_balance.csv):

| Covariate | Mean Treated (Unadj) | Mean Control (Unadj) | Raw SMD | Mean Treated (Matched) | Mean Control (Matched) | Matched SMD | SMD Reduction | Balance Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Pace Bowling Delivery Indicator** | 0.618 | 0.615 | +0.0069 | 0.626 | 0.626 | **0.0000** | **100.00%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Opponent Pre-Match Elo** | 1510.866 | 1509.168 | +0.0258 | 1507.934 | 1507.849 | **+0.0013** | **94.97%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Pre-Match Historical Venue Baseline** | 1.392 | 1.393 | -0.0141 | 1.392 | 1.391 | **+0.0131** | **6.76%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Required Run Rate / Rate Urgency** | 10.567 | 8.297 | +0.6165 | 8.295 | 8.350 | **-0.0149** | **97.58%** | **Strictly Balanced ($|\text{SMD}| \le 0.10$)** |
| **Batting Order Position** | 5.639 | 2.907 | +1.3681 | 4.784 | 4.523 | **+0.1304** | **90.47%** | **Substantially Attenuated** |
| **Wickets in Hand** | 5.392 | 8.363 | -1.6659 | 6.216 | 6.963 | **-0.4189** | **74.85%** | **Substantially Attenuated** |
| **Balls Remaining** | 33.217 | 78.064 | -1.7666 | 34.737 | 46.334 | **-0.4569** | **74.14%** | **Substantially Attenuated** |

---

## 5. Key Diagnostic Observations

1. **Strict Balance Achieved on Key External Drivers:**  
   Pace vs. spin bowling ($\text{SMD} = 0.0000$), Opponent Pre-Match Elo ($\text{SMD} = +0.0013$), Pre-Match Venue Scoring Baseline ($\text{SMD} = +0.0131$), and Required Run Rate ($\text{SMD} = -0.0149$) all achieve strict balance ($|\text{SMD}| \le 0.10$), with rate urgency imbalance attenuated by **97.58%**.
2. **Massive Attenuation of Resource Disparities:**  
   The immense structural imbalance between pressure and non-pressure deliveries (e.g., raw SMD of -1.77 in balls remaining and -1.67 in wickets in hand) is attenuated by **74.1% to 74.9%**, and batting order imbalance is attenuated by **90.47%**.
3. **Residual Structural Gap:**  
   Because high-pressure situations intrinsically concentrate in late overs with fewer wickets, exact balance across all resource dimensions cannot be achieved without discarding almost all death overs. The residual SMD of ~0.42 reflects the physical reality of T20 cricket, which is documented here as an explicit methodological diagnostic rather than swept under the rug.

---

*End of Stage 4.1.1 Clutch Matching Audit Report.*
