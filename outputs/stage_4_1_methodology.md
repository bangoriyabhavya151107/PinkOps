# PinkOps — Stage 4.1: Selection Framework & Player Evidence Methodology

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_1_methodology.md`  
**Stage:** 4.1 — Reliability Evidence & Selection Framework  
**Governance Status:** FROZEN METHODOLOGY (Anti-Collapse Framework Certified)  

---

## 1. Executive Summary & Purpose

The objective of Stage 4.1 is to transform the hardened match telemetry and delivery-level Value Added metrics into a transparent, competition-grade **Player Evidence and Selection Framework**. 

A central pathology in sports analytics is the premature scalar collapse—compressing multidimensional player behaviors into an uninterpretable composite score (e.g. an arbitrary "PinkOps Score" or linear weighted index). Such indices obscure critical operational distinctions, reward small-sample variance, and fail under tactical scrutiny.

Stage 4.1 implements the **Seven-Layer Decision Architecture**, preserves the uncollapsed 33-dimensional player evidence vector across 888 batters and 647 bowlers, incorporates the remediated attribution accounting and strengthened coarsened exact matching, and evaluates candidate aggregation frameworks without generating premature player rankings or auction picks.

---

## 2. The Formal Stage 4.1 Estimand

### 2.1 The Core Analytical Question
In Operation Pink Panther, player evaluation is explicitly formulated as:

> **"Which players provide the strongest evidence of reliable positive execution under pressure for the specific role and context relevant to the Rajasthan Royals selection problem?"**

This estimand decomposes into seven non-overlapping dimensions:
1. **Opportunity:** How much pressure did the player encounter? ($P(t^-) \in [0, 1]$, raw pressure balls $N_{\text{press}}$, weighted exposure $E^* = \sum P(t^-)$).
2. **Expected Outcome:** What would a professional average player achieve in the identical situational context? ($\hat{\mu}_B(t^-)$ under Frozen Specification B).
3. **Execution:** Did the player produce positive marginal output relative to expectation? (Batter Run Value Above Expectation $\text{RVA}$, Bowler Runs Conceded Suppression $\text{RCS}$, boundary rates, dot rates).
4. **Reliability & Downside:** Was positive execution repeatable across independent matches ($\text{MAD}, \text{IQR}$) while bounding catastrophe risk ($\text{EDR} \le 5$ balls for batters, $\text{BOR} \ge 15$ runs for bowlers)?
5. **Clutch Delta:** Did execution hold or elevate relative to a comparable matched baseline? (Descriptive context-adjusted pressure differential).
6. **Uncertainty & Evidence Depth:** How much confidence exists in the player estimate? (Empirical Bayes shrinkage $K = 100$, Lower Uncertainty Bound $\text{LUB}_{20}$, evidence tiers).
7. **Context & Role Alignment:** Under what environmental conditions did the player perform? (Tactical roles, phase splits, pace/spin facing %, opponent Elo).

### 2.2 Primary Expectation Estimand: Frozen Specification B
Following empirical investigation across all 200,961 normal-innings deliveries, **Specification B is formally frozen as the primary expectation estimand**:
$$\hat{\mu}_{\text{runs}}(t^-) = f_B(\mathbf{X}_B(t^-))$$
- **13 Pre-Delivery Features:** `innings_progress_before`, `wickets_in_hand_before`, `wickets_before`, `is_chase`, `is_powerplay`, `is_death`, `is_pace`, `venue_baseline` (shrunk $K=500$), `comp_baseline`, `home_pre_match_elo`, `away_pre_match_elo`, `batting_order`, `batter_balls_faced_before`.
- **Methodological Justification:** Specification B eliminates endogenous self-conditioning (where a batter's own recent boundaries raise the baseline against which they are immediately evaluated), while costing only $0.0022$ runs/ball in delivery MAE ($0.8146$ vs $0.8124$). Specification A is retained as an audited multiverse check.

---

## 3. Remediated Attribution Accounting

Following the Stage 4.0 review, all event attribution rules were remediated and verified across the 200,999 delivery dataset:

| Dimension | Remediated Accounting Rule | Governing Cricket Law |
|---|---|---|
| **Batter Runs** | Strictly `runs` (runs off the bat). Byes, leg-byes, wides, and penalty runs are excluded. | MCC Law 18 / 19 |
| **Bowler Runs Conceded** | Runs off bat + wides + no-balls (`Overstep`, `other`). Byes, leg-byes, and penalties are strictly excluded. | MCC Law 21 / 22 |
| **Bowler Wickets** | Strictly `is_bowler_wicket == 1` (`Caught`, `Bowled`, `LBW`, `Stump`, `Hit Wicket`). Run-outs ($600$), retire out ($6$), and obstructing the field ($3$) are excluded. | MCC Law 27 |
| **Batter Dismissals** | Stroke-execution dismissals isolated from non-standard running mix-ups (`RunOut`) and tactical exits (`Retire Out`). | Analytical Definition |
| **Retired Hurt** | 12 deliveries isolated as medical stoppages; zero wickets charged to team, zero wickets credited to bowler. | MCC Law 25 |

---

## 4. Candidate Aggregation Frameworks Evaluation

Stage 4.1 evaluated the five candidate aggregation methodologies:

### 4.1 Candidate A — Hurdle Gate + Conservative Evidence Ordering
- **Mechanism:** Imposes qualifying hurdles on sample exposure ($N \ge 150, N_{\text{press}} \ge 40$), downside risk ($\text{EDR} \le 0.20$ or $\text{BOR} \le 0.18$), and consistency ($\text{MAD} \le 0.60$), then orders qualified players on $\text{LUB}_{20}$.
- **Remediation:** Avoids brittle step-functions by utilizing soft governance tiers (Robust, Moderate, Sparse) and risk flags rather than permanent disqualification.

### 4.2 Candidate B — Constrained Multi-Objective Squad Optimization
- **Mechanism:** Formulates squad construction as an integer programming problem maximizing squad Value Added subject to squad-level risk caps, phase constraints, and uncertainty budgets.
- **Role:** Designated for squad-level portfolio construction, strictly distinguished from individual player evaluation.

### 4.3 Candidate C — Lower Uncertainty Bound (LUB) Ordering
- **Mechanism:** Orders players by $\text{LUB}_{20} = \hat{\theta}_i^{\text{EB}} - 0.842 \cdot \text{SE}_i^{\text{EB}}$.
- **Role:** Serves as the primary continuous uncertainty floor, evaluated alongside downside and consistency metrics.

### 4.4 Candidate D — Principal Component Analysis (PCA)
- **Mechanism:** Unsupervised factor decomposition across layers.
- **Governance Ruling:** **Formally prohibited as a primary decision or ranking metric** due to sign ambiguity and uninterpretable blending of failure modes. Retained solely as a diagnostic for collinearity.

### 4.5 Candidate E — Tiered Reliability Matrix
- **Mechanism:** Translates continuous evidence vectors into discrete, transparent tactical archetypes.
- **Role:** Selected as the communication layer for Rajasthan Royals decision-makers.

**Governance Decision:** A **hybrid synthesis of Candidate A (Governance Hurdles), Candidate C (LUB20 Ordering), and Candidate E (Tiered Profiles)** forms the Stage 4.1 decision architecture.

---

## 5. The Seven-Layer Decision Architecture

```
Layer 1: Evidence Sufficiency    ──► Classify into Robust (>=150/40), Moderate (>=50/15), Sparse (<50/15)
Layer 2: Performance Direction   ──► Evaluate EB Shrunk Estimate vs Population Expectation Baseline
Layer 3: Downside Risk Screen    ──► Screen Catastrophe Probability (Batter EDR <= 0.20, Bowler BOR <= 0.18)
Layer 4: Consistency Assessment ──► Measure Dispersion (MAD, IQR, Negative Match Contribution %)
Layer 5: Matched Clutch Delta   ──► Measure Context-Adjusted Differential (CEM Matched Baseline)
Layer 6: Tactical Role Context   ──► Segment by Tactical Role (Top-Order, Middle, Death, Pace vs Spin)
Layer 7: Decision Classification ──► Assign Evidence Profiles (Reliable, High-Upside, Context, Emerging, Concern)
```

---

## 6. Role-Specific Tactical Modeling

Players are not evaluated against a single undifferentiated standard. They are segmented into tactical roles:
- **Batters:**
  - *Top-Order Anchor / Powerplay Batter:* $\text{PP} \ge 40\%$ exposure or Order $1-3$.
  - *Middle-Overs Accelerator:* Middle-overs exposure $\ge 50\%$ or Order $4-6$.
  - *Finisher / Death Specialist:* Death-overs exposure $\ge 28\%$ or Order $5-8$.
- **Bowlers:**
  - *Powerplay Specialist (Pace / Spin):* Powerplay exposure $\ge 38\%$.
  - *Middle Enforcer (Pace / Spin):* Middle-overs exposure $\ge 50\%$.
  - *Death Specialist (Pace / Spin):* Death-overs exposure $\ge 30\%$.

---

## 7. Governance Invariants

- [x] **Zero Composite Scores:** No `pinkops_score`, `composite_score`, or arbitrary weighted average.
- [x] **Zero Premature Player Rankings:** No 1-to-N sorting or Top 10 lists generated.
- [x] **Zero Auction Recommendations:** No purse valuations assigned in Stage 4.1.
- [x] **Raw Competition Source Data Immutable:** `data/raw/` untouched.

*Document Approved by PinkOps Quantitative Governance Committee.*
