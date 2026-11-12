# PinkOps — Stage 3.0: Methodology Design Document
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Competition**: Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Author**: Lead Data Engineer  
**Status**: DRAFT / ARCHITECTURAL BLUEPRINT (Stage 3.0 Exploratory & Model-Design Phase)  

---

## Executive Summary & Architectural Purpose

This document establishes the scientific, mathematical, and data-engineering foundation for **Operation Pink Panther**. The overarching objective of PinkOps is to identify the most **reliable batters and bowlers under pressure** in T20 cricket using the audited competition dataset (200,999 deliveries across 867 contested matches from 2022 to 2026).

In accordance with strict Stage 3 governance:
- **No players are selected or ranked.**
- **No arbitrary pressure weights or ad-hoc thresholds are invented.**
- **No final PinkOps score is collapsed prematurely.**
- **Situation difficulty (environment) is strictly separated from player execution (performance).**
- **Every metric serves an explicit analytical purpose grounded in empirical cricket data.**

---

## 1. Definition of Pressure

### Conceptual Foundations
In conventional sports discourse, "pressure" is frequently conflated with subjective perceptions (e.g., "big names", "reputation", or "clutch moments"). In PinkOps, **pressure is defined objectively as the environmental stress imposed by the match state on the participating teams at a specific instant in time ($t^-$).**

Pressure in T20 cricket is continuous, dynamic, and multidimensional. It is fundamentally governed by four interacting physical and strategic dimensions:

1. **Stakes / Leverage ($\mathcal{L}$)**: The sensitivity of the match win probability to the outcome of the immediate delivery. A delivery where a wicket swings win probability by $\pm 25\%$ carries vastly higher leverage than a delivery where win probability swings by $\pm 0.5\%$.
2. **Resource Scarcity ($\mathcal{S}$)**: The depletion of available wickets in hand ($W_{\text{rem}} \in [1, 10]$) relative to balls remaining ($B_{\text{rem}} \in [1, 120]$). As wickets fall, the marginal cost of losing another wicket escalates non-linearly.
3. **Temporal Urgency / Rate Stress ($\mathcal{U}$)**: The deficit between required rate and baseline scoring rates. In chases, this is represented by Required Run Rate (RRR) and its divergence from Current Run Rate (CRR). In first innings, it is represented by death-over acceleration demands and recovery demands following early collapses.
4. **Asymmetry of Risk ($\mathcal{A}$)**: In high-pressure contexts, the cost of failure (a dot ball or dismissal) often dwarfs the value of a single run, altering the optimal risk-reward payoff for both batter and bowler.

### Rejection of Binary Classification
PinkOps explicitly rejects binary classifications ($\text{pressure} \in \{0, 1\}$). Categorizing an RRR of $10.01$ as "pressure" while $9.99$ is "non-pressure" introduces severe threshold bias, discards variance, and distorts player sample sizes. Instead, pressure is modeled as a **continuous intensity function** $P(t^-) \in [0, 1]$ or $[0, \infty)$ derived from pre-delivery covariates.

---

## 2. Definition of Pressure Opportunity

### Environmental Purity
A **pressure opportunity** represents an exogenous event wherein a player is exposed to a high-pressure match environment. 

$$\text{Opportunity}_i(t^-) = \mathbb{I}(\text{Player } i \text{ is active on delivery } t^-) \times \text{PressureIntensity}(t^-)$$

**Core Axiom of Separation**: The existence, intensity, and classification of a pressure opportunity depends **exclusively on the match state immediately preceding the delivery ($t^-$)**. A player's subsequent action (hitting a six, playing a dot, or getting out) has **zero mathematical influence** on the opportunity itself.

### Granularity of Exposure
Opportunities are tracked across three distinct granularities:
1. **Delivery-Level Exposure**: Cumulative deliveries faced (batters) or bowled (bowlers) weighted by delivery pressure intensity $\sum_t P(t^-)$.
2. **Over-Level Exposure**: Distinct overs bowled or faced in critical phases (e.g., death overs 16–20 or high-RRR phases).
3. **Innings/Match-Level Exposure**: Innings entered where the team was under acute resource deficit (e.g., entering at 25/3 in the powerplay) or chasing a steep target.

---

## 3. Definition of Expected Performance

### Baseline Expectation Function
Expected performance represents the conditional statistical expectation of a delivery outcome given the environmental context, assuming an **average competitive player** placed in that exact situation.

For any delivery $t$, let $\mathbf{X}(t^-)$ be the vector of pre-delivery environmental features:
$$\mathbf{X}(t^-) = [\text{InningsProgress}, \text{WicketsInHand}, \text{BallsRemaining}, \text{Phase}, \text{RecentScoring}, \text{VenueBaseline}, \text{CompBaseline}, \text{BowlingType}]$$

The expected outcomes are modeled as:
1. **Expected Runs**: $\mathbb{E}[R \mid \mathbf{X}(t^-)]$ (continuous, bounded $[0, 7]$)
2. **Expected Boundary Probability**: $\mathbb{P}(\text{Boundary} \mid \mathbf{X}(t^-)) = \sigma(\mathbf{w}_b^T \mathbf{X}(t^-))$
3. **Expected Dot-Ball Probability**: $\mathbb{P}(\text{Dot} \mid \mathbf{X}(t^-)) = \sigma(\mathbf{w}_d^T \mathbf{X}(t^-))$
4. **Expected Dismissal Probability**: $\mathbb{P}(\text{Wicket} \mid \mathbf{X}(t^-)) = \sigma(\mathbf{w}_w^T \mathbf{X}(t^-))$

These expectations are strictly out-of-sample and cross-validated across match-level folds to prevent memorization.

---

## 4. Definition of Actual Performance

Actual performance represents the realized empirical outcome of the delivery attributed to the active participants:
- **For Batters**:
  - Bat runs scored ($R_{\text{bat}} \in \{0, 1, 2, 3, 4, 5, 6\}$)
  - Boundary hit ($\mathbb{I}(R_{\text{bat}} \in \{4, 6\})$)
  - Dot ball played ($\mathbb{I}(R_{\text{bat}} = 0 \land \text{no byes/legbyes})$)
  - Dismissal suffered ($\mathbb{I}(\text{dismissed\_player\_id} = \text{striker\_id})$)
  - Strike retention / rotation (strike preserved for next ball)
- **For Bowlers**:
  - Total runs conceded ($R_{\text{total}} = R_{\text{bat}} + \text{wides} + \text{no-balls}$)
  - Bowler wicket taken ($\mathbb{I}(\text{bowler\_wicket} = 1)$, excluding run outs and retired hurt)
  - Dot ball bowled ($\mathbb{I}(R_{\text{total}} = 0)$)
  - Boundary conceded ($\mathbb{I}(\text{is\_four} \lor \text{is\_six})$)
  - Extras conceded (illegal delivery penalty)

---

## 5. Definition of Clutch / Pressure Delta

### Context-Adjusted Value Added
For any delivery $t$, the **Value Added (VA)** over expectation is:
$$\text{VA}_{\text{batter}}(t) = R_{\text{bat}}(t) - \mathbb{E}[R \mid \mathbf{X}(t^-)]$$
$$\text{VA}_{\text{bowler}}(t) = \mathbb{E}[R_{\text{conceded}} \mid \mathbf{X}(t^-)] - R_{\text{total}}(t)$$

### Matched Pressure Delta ($\Delta_{\text{Clutch}}$)
To determine whether a player possesses true "clutch" ability or merely benefits from friendly situations, we define the **Pressure Delta**:
$$\Delta_{\text{Clutch}} = \overline{\text{VA}}_{\text{High Pressure}} - \overline{\text{VA}}_{\text{Comparable Baseline}}$$

**Strict Matching Requirement**: A player cannot be compared against arbitrary global averages. The baseline must be matched on:
- Phase of the innings (Powerplay vs Middle vs Death)
- Batting order / entry point
- Bowling type (Pace vs Spin)
- Venue scoring baseline

This prevents a death-over finisher who naturally faces higher baseline RRR from being unfairly penalized or inflated compared to a top-order anchor.

---

## 6. Definition of Reliability

### Rejection of Simple Low Variance
In traditional statistics, reliability is often equated with low variance ($\sigma^2$). In elite sport, this definition is dangerously flawed: a batter who consistently scores 12 runs off 12 balls has low variance, but has a catastrophic negative impact in high-pressure chases.

### Multidimensional Reliability Architecture
PinkOps defines **Reliability ($\mathcal{R}$)** across four foundational pillars:
$$\mathcal{R} = f(\text{Execution Quality}, \text{Execution Stability}, \text{Evidence Depth}, \text{Downside Protection})$$

1. **Execution Quality Under Pressure**: Positive context-adjusted value added ($\overline{\text{VA}} > 0$) across high-pressure environments.
2. **Execution Stability (Consistency)**: Consistency of contribution across distinct matches and opponents, measured via match-level contribution Gini coefficient or interquartile range.
3. **Evidence Depth (Sample Volume)**: Cumulative volume of high-pressure deliveries faced/bowled. High performance over 20 balls is noise; high performance over 200 balls is skill.
4. **Downside Protection (Bust Rate)**: Minimization of catastrophic failure under pressure.
   - For Batters: Probability of an early dismissal (< 5 balls) in a pressure entry.
   - For Bowlers: Probability of conceding a blowout over (18+ runs) when defending close games.

---

## 7. Treatment of Uncertainty

### Statistical Realities of T20 Cricket
T20 cricket is characterized by high intrinsic stochasticity. A top-edge can fly for six or land safely between three fielders. In small samples, raw averages are dominated by luck.

### Uncertainty Mitigation Framework
PinkOps implements a tripartite uncertainty protocol:
1. **Empirical Bayes (EB) Shrinkage**: Individual player performance estimates $\hat{\theta}_i$ are shrunk toward the population prior $\mu_0$ as a function of their sample size $N_i$:
   $$\theta_i^{\text{shrunk}} = \frac{N_i}{N_i + K} \hat{\theta}_i + \frac{K}{N_i + K} \mu_0$$
   where $K$ represents the shrinkage parameter (equivalent to the number of pseudo-observations required for the player's observed data to outweigh the prior).
2. **Bootstrap Resampling**: For every player, 1,000 cluster-bootstrapped resamples (clustered by match) are drawn to generate 95% empirical confidence intervals $[\theta_{i, 0.025}, \theta_{i, 0.975}]$.
3. **Lower Confidence Bound (LCB) Ranking**: In decision-making, players are evaluated by their conservative performance estimate (e.g., 20th percentile of posterior distribution), naturally penalizing noisy small samples without discarding them.

---

## 8. Treatment of Sample Size

### Rejection of Arbitrary Truncation
Imposing rigid cutoffs (e.g., "minimum 100 balls") catastrophically distorts player discovery. In T20 cricket:
- A #7 finisher may face only 8–12 balls per match, accumulating only 60 balls across an entire season.
- An elite death bowler bowling overs 18 and 20 accumulates only 12 balls per match.
Hard cutoffs discard the exact role-specialists most critical to high-pressure outcomes.

### Empirical Exposure Profiling
Instead of arbitrary exclusion:
1. We profile the empirical distribution of player opportunities across the entire 867-match corpus.
2. All players are retained in the master analytical framework.
3. Sample size is incorporated continuously through Bayesian shrinkage and uncertainty penalties, ensuring that a player with 40 exceptional pressure balls is recognized as a high-potential specialist with wide error bars, rather than erased from analysis.

---

## 9. Opposition-Strength Methodology

### Rejection of Manual Tiering
Manual league or team ratings (e.g., "IPL is Tier 1, Associate is Tier 3") introduce subjective bias. PinkOps implements an **empirical, data-grounded strength framework**.

### Dynamic Pre-Match Elo Ratings
Each team's strength is tracked via an Elo rating system that updates strictly **chronologically**:
- Initial baseline rating: $R_0 = 1500.0$
- Before match $m$ on date $D_m$, pre-match win expectancy:
  $$\mathbb{P}(\text{Win}_A) = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$
- Post-match rating update with $K = 32.0$:
  $$R_A \leftarrow R_A + K \cdot (S_A - \mathbb{P}(\text{Win}_A))$$
- **Zero Circular Leakage**: The rating attached to match $m$ is strictly $R(t^-)$ prior to coin toss. Subsequent outcomes never back-propagate into historical ratings.

### Opponent Bowling/Batting Attack Adjustments
Deliveries are adjusted for the specific quality of the opponent attack:
- Bowler quality faced by batter: Shrunk historical dot-ball and economy rate of the bowler prior to match date.
- Batter quality faced by bowler: Shrunk historical strike rate and boundary rate of the batter prior to match date.

---

## 10. Competition-Strength Methodology

### Scoring Environment Variation
Across the 138 competitions in the dataset, scoring baselines vary significantly:
- IPL 2026: Mean runs per ball = $1.566$, Boundary rate = $21.4\%$, Dot rate = $31.1\%$
- IPL 2022: Mean runs per ball = $1.362$, Boundary rate = $17.2\%$, Dot rate = $35.5\%$
- Asia Cup 2025: Mean runs per ball = $1.242$, Boundary rate = $13.8\%$, Dot rate = $37.5\%$

### Competition Centering
Rather than penalizing players for competing in lower-scoring international tournaments, all expected performance models include competition fixed/shrunk baselines, ensuring that value-added metrics measure performance relative to the competition environment.

---

## 11. Venue Normalization Methodology

### The Low-Sample Venue Challenge
The dataset encompasses 97 distinct venues, but sample sizes are highly skewed:
- Top 5 venues host 187 matches (~44,600 balls).
- 25% of venues host 3 or fewer matches; 12 venues host exactly 1 match.
Using raw venue averages would severely overfit small-sample anomalies (e.g., Venue 3333 with 64 balls at $0.969$ runs/ball).

### Empirical Bayes Venue Shrinkage
Every venue's scoring parameter $\hat{\mu}_v$ is shrunk toward the global format baseline $\mu_{\text{global}}$:
$$\mu_v^{\text{shrunk}} = \frac{N_v}{N_v + K_{\text{venue}}} \bar{x}_v + \frac{K_{\text{venue}}}{N_v + K_{\text{venue}}} \mu_{\text{global}}$$
where $K_{\text{venue}} = 500$ deliveries (~2 full matches). For venues with thousands of balls, the empirical mean dominates; for single-match venues, the estimate reverts safely to baseline.

---

## 12. Batter Methodology

### Delivery-Level Decomposition
Batter performance is evaluated across a multi-objective matrix:
1. **Run Value Added (RVA)**: $\text{RVA} = R_{\text{bat}} - \mathbb{E}[R \mid \text{state}]$.
2. **Boundary Generation Rate over Expectation (BGRE)**: $\mathbb{I}(\text{Boundary}) - \mathbb{P}(\text{Boundary} \mid \text{state})$.
3. **Dot-Ball Avoidance Rate (DBAR)**: $\mathbb{P}(\text{Dot} \mid \text{state}) - \mathbb{I}(\text{Dot})$.
4. **Wicket Preservation Value (WPV)**: In crisis situations, surviving delivery $t$ without getting out carries positive equity.
5. **Strike Rotation Utility**: Generating singles in non-boundary deliveries, turning the strike over to partner without stalling momentum.

---

## 13. Bowler Methodology

### Delivery-Level Decomposition
Bowler performance under pressure is evaluated across complementary defensive and attacking dimensions:
1. **Runs Conceded Suppression (RCS)**: $\mathbb{E}[R_{\text{conceded}} \mid \text{state}] - R_{\text{total}}$.
2. **Dot-Ball Creation Rate (DBCR)**: $\mathbb{I}(\text{Dot}) - \mathbb{P}(\text{Dot} \mid \text{state})$.
3. **Boundary Suppression Rate (BSR)**: $\mathbb{P}(\text{Boundary} \mid \text{state}) - \mathbb{I}(\text{Boundary})$.
4. **Wicket Taking Probability over Expectation (WTPE)**: $\mathbb{I}(\text{BowlerWicket}) - \mathbb{P}(\text{Wicket} \mid \text{state})$.
5. **Discipline / Extra Prevention**: Avoiding illegal deliveries (wides, oversteps, beamers) that yield extra runs and reset legal ball counters.

---

## 14. First-Innings Methodology: Resource-Scarcity & Crisis Framework

### Elimination of Fabricated Targets
The first innings features no scoreboard target and no Required Run Rate. Imputing a synthetic target introduces arbitrary assumptions.

### Empirical Crisis & Urgency Metrics
First-innings pressure is modeled empirically via:
1. **Resource Depletion Index (RDI)**:
   $$\text{RDI}(t^-) = \frac{\text{WicketsLost}(t^-)}{\text{InningsProgress}(t^-) + 0.15}$$
   Spikes dramatically during top-order collapses (e.g., 20/3 in over 4 yields $\text{RDI} \approx 8.5$, vs normal $1.5$).
2. **Par-Score Trajectory Deficit**: Expected innings total based on pre-delivery state minus historical venue average.
3. **Death Acceleration Demand**: Balls remaining in overs 16–20 relative to wickets in hand.

---

## 15. Chase Methodology: Dynamic Chase Equation & Leverage

### The Physics of Chasing
In the second innings, every ball alters the exact relationship between runs needed and balls remaining:
$$\text{RunsRequired}(t^-) = \text{Target} - \text{RunsScored}(t^-)$$
$$\text{RRR}(t^-) = \frac{\text{RunsRequired}(t^-)}{\text{BallsRemaining}(t^-) / 6.0}$$

### Win Probability Leverage Index (WPLI)
Using a match-grouped logistic win probability model $P(\text{Win} \mid \mathbf{X}_{\text{chase}})$, the **Leverage Index** is defined as the expected root-mean-square change in win probability over possible delivery outcomes:
$$\text{WPLI}(t^-) = \frac{\Delta \text{WP}_{\text{wicket}} + \Delta \text{WP}_{\text{six}}}{2 \cdot \sigma_{\text{baseline}}(\text{WP})}$$
- $\text{WPLI} \gg 1.0$: High leverage (nail-biter finishes).
- $\text{WPLI} \ll 1.0$: Low leverage (blowouts where outcome is decided).

---

## 16. Super Over Treatment

### Empirical Justification for Complete Isolation
The Stage 2/2.1 dataset contains 6 Super Over matches (Innings 3 & 4, 38 deliveries). Empirical analysis reveals:
- Innings 3 wicket rate: **48.0%** (12 wickets in 25 balls!).
- Dot ball rate: **56.0%**.
- Batters have only 2 wickets in hand and swing maximally from ball 1.

### Policy
1. **Super Overs are excluded from regular T20 model training.** Including them would distort standard wicket and scoring probability distributions.
2. **Super Overs are retained as dedicated qualitative stress tests.** Performance in Super Overs will be reported as an independent micro-sample indicator.

---

## 17. Validation Strategy

### Cross-Validation Architecture
To prevent optimistic leakage:
1. **Match-Grouped K-Fold (5-Fold)**: All deliveries from a given match are strictly assigned to either Train or Test. Deliveries from the same match never bridge folds.
2. **Temporal Split Validation**: Train on seasons 2022–2024 (497 matches, ~116,000 balls); validate on seasons 2025–2026 (354 matches, ~80,500 balls).
3. **Leave-One-Competition-Out (LOCO)**: Validate generalization across IPL vs international fixtures.

### Calibration & Error Metrics
- Continuous models ($E[R]$): Mean Absolute Error (MAE), Root Mean Squared Error (RMSE).
- Probabilistic models ($P(\text{Win}), P(\text{Boundary}), P(\text{Dot}), P(\text{Wicket})$): LogLoss, Brier Score, and Expected Calibration Error (ECE) across decile bins.

---

## 18. Leakage Controls

### Causal Timeline Gate
Every feature fed into an expectation or pressure model must satisfy the **Strict Pre-Delivery Invariant**:
$$\text{FeatureTimestamp} \le t^- < t_{\text{delivery\_bowled}}$$

Strictly prohibited from pre-delivery feature vectors:
- `runs_on_delivery`, `is_four`, `is_six`, `is_wicket`, `extras1_runs`
- `post_match_winner_team_id`, `post_match_result`, `post_margin_value`
- `post_innings_total_runs`, `post_innings_total_wickets`
- Future delivery outcomes within the over or match.

---

## 19. Sensitivity Analysis

Before finalizing Stage 4 model configurations, we conduct systematic sensitivity sweeps across:
1. **Shrinkage Parameter $K$**: Testing stability across $K \in [20, 50, 100, 200]$.
2. **Continuous Pressure Exponent**: Testing linear vs quadratic scaling of RRR stress.
3. **Opposition Weighting Scale**: Testing Elo scaling factors ($K_{\text{elo}} \in [16, 32, 48]$).

---

## 20. Robustness Testing & Specification-Curve Framework

### Invariance Across Model Specifications
Conclusions must not hinge on idiosyncratic modeling choices. We design a **Multiverse Specification Grid**:
- Specification 1: Linear Ridge regression expectation + Empirical Bayes shrinkage.
- Specification 2: Logistic Win Probability Leverage + Elo opponent adjustment.
- Specification 3: Phase-matched stratified empirical expectation.
- Specification 4: Leave-one-season-out temporal cross-validation model.

**Candidate Selection Stability Metric**: A player will only be considered robustly reliable if they maintain elite tier performance across $\ge 80\%$ of valid specification curves.

---
*Stage 3.0 Methodology Blueprint Approved for Implementation by PinkOps Data Engineering.*
