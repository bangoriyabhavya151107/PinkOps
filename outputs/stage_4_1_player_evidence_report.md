# PinkOps — Stage 4.1: Player Evidence & Multi-Dimensional Reliability Report
**Project:** Operation Pink Panther  
**Brand:** PinkOps  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Tagline:** Finding the Next Legend  
**Working Slogan:** Zero Choke. All Smoke.  
**Date:** November 2026  
**Status:** Frozen Stage 4.1 Evidence Specification (Spec B Canonical)

---

## Executive Summary & Non-Negotiable Governance Boundary

This report delivers the **uncollapsed, multi-dimensional player evidence profiles** constructed in accordance with the Stage 4.0 Reliability Architecture and Stage 4.1 Execution Framework. 

> [!IMPORTANT]
> **GOVERNANCE NOTICE: ZERO SINGLE-SCORE RANKINGS**  
> In strict compliance with the competition mandate and the frozen Stage 4.0 estimand specification, **NO single composite "PinkOps Score" has been computed, NO linear ranking (1 to $N$) is produced, and NO "Top 10" player lists are presented in this report.** Player reliability under high-leverage conditions is intrinsically multi-dimensional; collapsing performance into a scalar score conceals critical failure modes (e.g., high early-dismissal rates or extreme match-to-match variance) and violates scientific validity. Auction valuation and role-specific selection are deferred to Stage 5.

All metrics reported herein are derived from the canonical modeling universe of **200,961 normal-innings deliveries** across **867 contested matches** (reconciled against the raw 200,999 delivery dataset by strictly isolating 38 Super Over deliveries into an independent low-sample audit register).

---

## 1. Population Evidence Tier & Reliability Profile Distribution

The Stage 4.1 pipeline processes **1,535 total player entries** (888 batter entries, 647 bowler entries). Players are first stratified into three sample-size evidence tiers to prevent small-sample noise from polluting decision-making:

- **Robust Evidence Tier** ($\ge 250$ total opportunities & $\ge 75$ high-pressure opportunities): 180 batters, 241 bowlers.
- **Moderate Evidence Tier** ($100-249$ total opportunities & $\ge 20$ high-pressure opportunities): 120 batters, 74 bowlers.
- **Low / Anecdotal Evidence Tier** ($< 100$ total opportunities or $< 20$ high-pressure opportunities): 588 batters, 332 bowlers.

### Population Profile Summary
```
+-----------------------------------+----------------+----------------+----------------+
| Reliability Profile               | Batters        | Bowlers        | Total Entries  |
+-----------------------------------+----------------+----------------+----------------+
| Reliable Pressure Performer       | 14             | 51             | 65             |
| High-Upside / Higher-Risk         | 18             | 9              | 27             |
| Context Specialist                | 28             | 3              | 31             |
| Emerging Evidence                 | 7              | 15             | 22             |
| Pressure Concern                  | 321            | 287            | 608            |
| Neutral / Insufficient Evidence   | 500            | 282            | 782            |
+-----------------------------------+----------------+----------------+----------------+
| Total Entries                     | 888            | 647            | 1,535          |
+-----------------------------------+----------------+----------------+----------------+
```

---

## 2. Multi-Dimensional Evidence Dimensions

Each player is represented by a **33-dimensional uncollapsed evidence vector** capturing seven independent facets of pressure performance:

1. **Volume & Exposure:** Total deliveries faced/bowled ($n_{\text{tot}}$), high-pressure deliveries faced/bowled ($n_{\text{press}}$), pressure opportunity share ($p_{\text{opp}}$).
2. **Conservative Performance (LUB20):** Empirical Bayes shrunk mean value-added minus 0.842 standard errors ($\text{LUB}_{20} = \hat{\mu}_{\text{EB}} - 0.842 \cdot \text{SE}_{\text{EB}}$), guaranteeing an 80% one-sided lower credible bound against small-sample inflation.
3. **Consistency & Dispersion:** Match-level Value-Added Median Absolute Deviation ($\text{MAD}$), Interquartile Range ($\text{IQR}$), and Coefficient of Variation ($\text{CV}$).
4. **Catastrophic Tail Risk:** Early Dismissal Rate ($\text{EDR}$, dismissal in balls 1–5 under pressure for batters) and Pressure Blowout Rate ($\text{BOR}$, conceding $\ge 12$ runs/over under pressure for bowlers).
5. **Clutch Invariance:** Coarsened Exact Matched Relative Value Added ($\Delta_{\text{RVA}} = \text{RVA}_{\text{pressure}} - \text{RVA}_{\text{low\_pressure}}$), evaluating whether performance elevates or degrades relative to identical game situations under low pressure.
6. **Tactical Role Specialization:** Phase-stratified output across Powerplay (overs 1–6), Middle overs (7–15), and Death overs (16–20), partitioned by bowling type (Pace vs. Spin).
7. **Multiverse Robustness:** Fraction of the 24 multiverse grid branches (varying pressure cutoffs, shrinkage priors, opposition adjustments, and LUB quantiles) supporting positive added value.

---

## 3. Batting Profiles Across Tactical Roles

### 3.1 Reliable Pressure Performers (Batting)
Criteria: Robust Evidence Tier, $\text{LUB}_{20} > 0.0$, Early Dismissal Rate $\le 20\%$, Match $\text{MAD} \le 0.55$, Multiverse Stability $= 8/8$ base branches.

| Player Name | Tactical Role | Pressure Balls ($n_{\text{press}}$) | Mean VA / Ball | $\text{LUB}_{20}$ VA | Early Dism. Rate | Match MAD | Clutch $\Delta_{\text{RVA}}$ | Multiverse Specs |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Naman Dhir** | Finisher / Death Specialist | 291 | +0.244 | **+0.192** | 17.4% | 0.406 | +0.183 | 8 / 8 |
| **Tim David** | Finisher / Death Specialist | 735 | +0.166 | **+0.133** | 19.4% | 0.525 | +0.125 | 8 / 8 |
| **Jitesh Sharma** | Finisher / Death Specialist | 438 | +0.154 | **+0.110** | 17.8% | 0.345 | +0.142 | 8 / 8 |
| **Suryakumar Yadav** | Middle-Overs Accelerator | 908 | +0.120 | **+0.089** | 16.5% | 0.353 | +0.098 | 8 / 8 |
| **Yashasvi Jaiswal** | Top-Order Anchor / PP | 77 | +0.167 | **+0.080** | 14.6% | 0.288 | +0.141 | 8 / 8 |
| **Dinesh Karthik** | Finisher / Death Specialist | 465 | +0.095 | **+0.063** | 18.2% | 0.362 | +0.071 | 8 / 8 |
| **Rajat Patidar** | Middle-Overs Accelerator | 520 | +0.087 | **+0.057** | 17.1% | 0.312 | +0.065 | 8 / 8 |
| **Marcus Stoinis** | Finisher / Death Specialist | 580 | +0.072 | **+0.044** | 18.9% | 0.410 | +0.052 | 8 / 8 |
| **Will Jacks** | Middle-Overs Accelerator | 312 | +0.081 | **+0.041** | 19.2% | 0.380 | +0.060 | 8 / 8 |
| **Ramandeep Singh** | Finisher / Death Specialist | 215 | +0.084 | **+0.034** | 16.7% | 0.320 | +0.075 | 8 / 8 |

*Key Takeaway:* Batters in this profile demonstrate high conservative efficiency without excessive tail risk. Yashasvi Jaiswal combines top-order powerplay pressure absorption with remarkably low dispersion ($\text{MAD} = 0.288$) and the lowest early-dismissal rate among openers (14.6%). Middle-order anchors like Suryakumar Yadav maintain positive value added across massive exposure (908 pressure balls faced) while remaining robust across 100% of multiverse specifications.

---

### 3.2 High-Upside / Higher-Risk Batters
Criteria: Robust Evidence Tier, $\text{LUB}_{20} > 0.0$, but exhibit Early Dismissal Rate $> 20\%$ OR Match $\text{MAD} > 0.55$.

| Player Name | Tactical Role | Pressure Balls | Mean VA | $\text{LUB}_{20}$ VA | Early Dism. Rate | Match MAD | Risk Profile Narrative |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Glenn Maxwell** | Middle Accelerator | 360 | +0.106 | +0.058 | **30.7%** | 0.507 | Extreme ceiling, but dismissed inside 5 balls in 30.7% of pressure entries. |
| **Andre Russell** | Finisher / Death | 542 | +0.158 | +0.119 | **21.1%** | 0.548 | Elite run-rate acceleration under pressure offset by elevated match-level variance. |
| **Fakhar Zaman** | Middle Accelerator | 295 | +0.118 | +0.065 | 10.6% | **0.342** | Elevated phase dependency; high output in chase phases with spin match-ups. |
| **Sikandar Raza** | Middle Accelerator | 654 | +0.062 | +0.026 | **21.1%** | 0.330 | Consistent middle contributor with moderate vulnerability to express pace early. |

*Tactical Deployment:* High-upside batters provide game-breaking win-probability shifts when they survive their initial entry, but require structured batting orders with protective anchors to mitigate catastrophic top-order collapses.

---

### 3.3 Context Specialists & Emerging Evidence Batters
- **Jake Fraser-McGurk (Top-Order Anchor / Powerplay):** Exhibits phenomenal raw acceleration under pressure (+0.314 Mean VA), but operates in the Moderate Evidence Tier (20 pressure deliveries faced) with an early dismissal rate of 30.4% and high volatility ($\text{MAD} = 0.721$). Classified as a *Context Specialist* suited for unconstrained chase phases rather than collapse recovery.
- **Rashid Khan (Finisher / Death Specialist):** Demonstrates death-overs batting utility (+0.130 $\text{LUB}_{20}$) but carries an early dismissal rate of 26.8% due to boundary-seeking intent from ball one.
- **Emerging Batters:** Ijaz Ahmadzai (114 pressure balls, $+0.030$ $\text{LUB}_{20}$) and Benjamin Calitz (52 pressure balls, $+0.022$ $\text{LUB}_{20}$, 0.0% early dismissal rate) warrant continued tracking in domestic circuits.

---

## 4. Bowling Profiles Across Tactical Roles

### 4.1 Reliable Pressure Performers (Bowling)
Criteria: Robust Evidence Tier, $\text{LUB}_{20} > 0.0$, Pressure Blowout Rate $\le 20\%$, Match $\text{MAD} \le 0.45$, Multiverse Stability $= 8/8$ base branches.

| Player Name | Tactical Role | Pressure Balls ($n_{\text{press}}$) | Mean VA / Ball | $\text{LUB}_{20}$ VA | Pressure Blowout Rate | Match MAD | Clutch $\Delta_{\text{RVA}}$ | Multiverse Specs |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sunil Narine** | Middle Enforcer (Spin) | 687 | +0.320 | **+0.285** | **5.5%** | 0.231 | +0.274 | 8 / 8 |
| **Jasprit Bumrah** | Death Specialist (Pace) | 697 | +0.320 | **+0.285** | **6.6%** | 0.243 | +0.268 | 8 / 8 |
| **Abrar Ahmed** | Middle Enforcer (Spin) | 359 | +0.203 | **+0.156** | 5.4% | 0.329 | +0.145 | 8 / 8 |
| **Matheesha Pathirana** | Death Specialist (Pace) | 698 | +0.180 | **+0.145** | 11.3% | 0.304 | +0.138 | 8 / 8 |
| **Jamie Overton** | Death Specialist (Pace) | 269 | +0.194 | **+0.140** | 12.9% | 0.440 | +0.130 | 8 / 8 |
| **Mustafizur Rahman** | Death Specialist (Pace) | 712 | +0.165 | **+0.135** | 11.8% | 0.298 | +0.128 | 8 / 8 |
| **Bhuvneshwar Kumar** | Powerplay Specialist (Pace) | 610 | +0.148 | **+0.114** | 8.2% | 0.275 | +0.109 | 8 / 8 |
| **Nathan Ellis** | Death Specialist (Pace) | 480 | +0.135 | **+0.103** | 10.4% | 0.280 | +0.098 | 8 / 8 |
| **Mohsin Khan** | Powerplay Specialist (Pace) | 320 | +0.145 | **+0.103** | 9.5% | 0.265 | +0.110 | 8 / 8 |
| **Varun Chakravarthy**| Middle Enforcer (Spin) | 650 | +0.132 | **+0.099** | 8.8% | 0.285 | +0.095 | 8 / 8 |

*Key Takeaway:* Jasprit Bumrah (Pace) and Sunil Narine (Spin) establish the statistical ceiling of pressure reliability in modern T20 cricket, both delivering an unmatched $\text{LUB}_{20} = +0.285$ runs saved per ball across nearly 700 pressure deliveries, with blowout rates contained below 7%. Pathirana and Mustafizur provide exceptional death-overs leverage, while Bhuvneshwar Kumar and Mohsin Khan dominate the high-pressure powerplay phases.

---

### 4.2 High-Upside / Higher-Risk Bowlers
| Player Name | Tactical Role | Pressure Balls | Mean VA | $\text{LUB}_{20}$ VA | Blowout Rate | Match MAD | Risk Profile Narrative |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Kyle Jamieson** | Powerplay Specialist (Pace) | 206 | +0.136 | +0.075 | **20.8%** | 0.309 | Elite swing and bounce, but elevated boundary leakage when lengths miss. |
| **Marco Jansen** | Powerplay Specialist (Pace) | 487 | +0.110 | +0.069 | **19.5%** | 0.279 | High strike power with the new ball; vulnerability to late-over death adjustments. |
| **Andile Phehlukwayo**| Death Specialist (Pace) | 46 | +0.103 | +0.003 | **25.0%** | 0.396 | High death-wicket upside coupled with 25% blowout rate under extreme pressure. |
| **Shamar Joseph** | Death Specialist (Pace) | 181 | +0.056 | -0.009 | **20.3%** | 0.270 | Raw pace disrupts batters, but line instability increases blowout probability. |

---

### 4.3 Context Specialists & Emerging Bowlers
- **Sakib Hussain (Death Specialist - Pace):** Robust Evidence Tier with high conservative output ($\text{LUB}_{20} = +0.138$, $\text{MAD} = 0.170$), but demonstrates distinct venue and chase-phase sensitivities.
- **Sonny Baker (Death Specialist - Pace):** Moderate Evidence Tier (42 pressure balls) showing outstanding control ($\text{LUB}_{20} = +0.073$, $\text{MAD} = 0.118$).
- **Ashton Agar (Middle Enforcer - Spin):** Moderate Evidence Tier (77 pressure balls) with $+0.059$ $\text{LUB}_{20}$ and 0.0% blowout rate under middle-overs pressure.

---

## 5. High-Volume vs. High-Efficiency Contrast

A critical flaw of naive ranking models is confounding *high sample volume* with *high pressure reliability*. The uncollapsed Stage 4.1 evidence matrix disentangles exposure from efficiency:

### High-Volume Anchors vs. High-Efficiency Impact Performers
```
Batters:
• Suryakumar Yadav: 908 pressure balls faced | +0.089 LUB20 | 16.5% EDR | 8/8 Multiverse Specs (High-Volume Anchor)
• Naman Dhir:       291 pressure balls faced | +0.192 LUB20 | 17.4% EDR | 8/8 Multiverse Specs (High-Efficiency Accelerator)

Bowlers:
• Jasprit Bumrah:   697 pressure balls bowled | +0.285 LUB20 |  6.6% BOR | 8/8 Multiverse Specs (High-Volume Sovereign)
• Jamie Overton:    269 pressure balls bowled | +0.140 LUB20 | 12.9% BOR | 8/8 Multiverse Specs (High-Efficiency Death Striker)
```
In Stage 5 squad assembly, high-volume anchors provide baseline roster stability, while high-efficiency impact performers provide targeted leverage against high-quality opposition.

---

## 6. Audit Trail & Data Links

- **Canonical Match-State Source:** [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet)
- **Player Evidence Matrix (33 Cols):** [`data/processed/stage_4_1_player_evidence.parquet`](file:///D:/PinkOps/data/processed/stage_4_1_player_evidence.parquet)
- **Player Classifications:** [`data/processed/stage_4_1_player_classifications.csv`](file:///D:/PinkOps/data/processed/stage_4_1_player_classifications.csv)
- **Multiverse Results:** [`data/processed/stage_4_1_robustness_results.csv`](file:///D:/PinkOps/data/processed/stage_4_1_robustness_results.csv)
- **Execution Methodology:** [`outputs/stage_4_1_methodology.md`](file:///D:/PinkOps/outputs/stage_4_1_methodology.md)
- **Validation Report:** [`outputs/stage_4_1_validation_report.md`](file:///D:/PinkOps/outputs/stage_4_1_validation_report.md)

*End of Stage 4.1 Player Evidence Report.*
