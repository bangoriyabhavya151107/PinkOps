# PinkOps — Stage 4.0: The Seven-Layer Reliability Architecture

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_reliability_architecture.md`  
**Stage:** 4.0 — Reliability Architecture, Estimand Freeze & Governance  
**Governance Status:** FROZEN ARCHITECTURE (Zero Player Rankings Generated)  

---

## 1. Architectural Philosophy: The Anti-Collapse Mandate

A catastrophic failure pattern in sports analytics is the **premature scalar collapse**—compressing a multidimensional vector of player behaviors into a single composite number (e.g., an arbitrary "PinkOps Index" or "Clutch Score") before understanding how the component signals behave. Such scalar metrics obscure vital operational distinctions:
- A high average run-scorer who regularly gets dismissed for a duck in critical playoff chases looks identical to a batter who consistently delivers 18 runs off 10 balls when required.
- A bowler who bowls 3 dots and gets hit for two sixes every over looks identical to a bowler who concedes 5 singles.
- A player with 15 balls of high-pressure data looks indistinguishable from a veteran with 350 high-pressure balls if uncertainty is ignored.

To prevent these distortions, Stage 4.0 establishes the **Seven-Layer Reliability Architecture**. Each layer encapsulates a distinct statistical phenomenon, strictly isolates its inputs and outputs, and passes its uncollapsed vector forward. 

```
                                 [ MATCH TELEMETRY (t^-) ]
                                             │
               ┌─────────────────────────────┴─────────────────────────────┐
               ▼                                                           ▼
     [ LAYER 1: OPPORTUNITY ]                                    [ LAYER 2: EXPECTATION ]
     - P(t^-) Intensity in [0, 1]                                 - Population Expectation mu_B(t^-)
     - Raw Count (N_press)                                       - Venue & Comp Baselines
     - Weighted Exposure (E*)                                    - Opponent Elo Adjustment
               │                                                           │
               └─────────────────────────────┬─────────────────────────────┘
                                             ▼
                                   [ LAYER 3: EXECUTION ]
                                   - Actual Outcome Y(t)
                                   - Value Added: VA(t) = Y(t) - mu_B(t^-)
                                   - Batter RVA / Bowler RCS
                                             │
                                             ▼
                                   [ LAYER 4: RELIABILITY ]
                 ┌───────────────────────────┼───────────────────────────┐
                 ▼                           ▼                           ▼
        [ DOWNSIDE RISK ]             [ CONSISTENCY ]             [ CLUTCH DELTA ]
        - Early Dismissal %           - Match VA MAD / IQR        - VA(Press) - VA(Base)
        - Blowout Over % (>=15)       - Negative Match %          - Matched Phase & Role
                 └───────────────────────────┬───────────────────────────┘
                                             ▼
                             [ LAYER 5: EVIDENCE & UNCERTAINTY ]
                             - Empirical Bayes Shrinkage (K = 100)
                             - Effective SE Calculation
                             - Lower Credible Bounds (LCB10, LCB20, LCB25, LCB30)
                                             │
                                             ▼
                                [ LAYER 6: CONTEXT & TIERS ]
                             - Sample Depth Tiers (Robust, Moderate, Sparse)
                             - Phase Splits (% PP, % Mid, % Death)
                             - Opposition & Venue Difficulty Adjustments
                             - Super Over Qualitative Annotations
                                             │
                                             ▼
                                [ LAYER 7: DECISION INTERFACE ]
                             - Uncollapsed Evidence Vector Export
                             - Candidate Aggregation Interfaces (A, B, C, D, E)
                             - STRICT GOVERNANCE: ZERO Composite Score in Stage 4.0
```

---

## 2. Layer 1: Opportunity Layer (Situational Pressure)

### 2.1 Responsibilities
The Opportunity Layer isolates the situational stress of the match state from player capability. It answers: *Under what environmental conditions did the player participate, and how intense was the competitive leverage?*

### 2.2 Mathematical Specifications
For each delivery $t$ at time $t^-$ (prior to the ball being bowled):
1. **Continuous Pressure Intensity $P(t^-) \in [0, 1]$:**
   $$P(t^-) = 0.35 \cdot \text{RDI}_{\text{norm}}(t^-) + 0.35 \cdot \text{Leverage}(t^-) + 0.15 \cdot \text{Phase}(t^-) + 0.15 \cdot \text{Wickets}(t^-)$$
2. **Binary High-Pressure Indicator:**
   $$I_{\text{press}}(t^-) = \mathbb{I}(P(t^-) \ge 0.50)$$
3. **Cumulative Exposure:**
   - Raw Total Deliveries: $N_{i,\text{total}} = \sum_{t \in \mathcal{D}_i} 1$
   - Raw Pressure Deliveries: $N_{i,\text{press}} = \sum_{t \in \mathcal{D}_i} I_{\text{press}}(t^-)$
   - Continuous Weighted Exposure: $E_i^* = \sum_{t \in \mathcal{D}_i} P(t^-)$
   - High-Pressure Ratio: $\text{HPR}_i = \frac{N_{i,\text{press}}}{N_{i,\text{total}}}$

### 2.3 Layer Invariant
**Invariant 1.1:** $P(t^-)$ depends strictly on match state $( \text{balls remaining}, \text{runs required}, \text{wickets in hand}, \text{innings}, \text{venue}, \text{competition} )$. It possesses **zero dependence** on the active batter's identity or the bowler's identity.

---

## 3. Layer 2: Expectation Layer (Contextual Population Baseline)

### 3.1 Responsibilities
The Expectation Layer models the expected counterfactual outcome of an average professional player facing the exact same situational, environmental, and opposition context.

### 3.2 Primary Estimand: Frozen Specification B
Following empirical validation (Section 3 of `stage_4_0_reliability_estimand.md`), Specification B is frozen as primary:
$$\hat{\mu}_{\text{runs}}(t^-) = f_B(\mathbf{X}_B(t^-))$$
where $\mathbf{X}_B(t^-)$ contains 13 pre-delivery features:
1. `innings_progress_before`: Delivery fraction completed ($0.0$ to $1.0$).
2. `wickets_in_hand_before`: Integer in $[1, 10]$.
3. `wickets_before`: Wickets fallen ($0$ to $9$).
4. `is_chase`: Binary ($1$ if 2nd innings, $0$ if 1st innings).
5. `is_powerplay`: Binary ($1$ if overs 0–5).
6. `is_death`: Binary ($1$ if overs 16–19).
7. `is_pace`: Binary bowling type.
8. `venue_baseline`: Shrunken historical run rate at venue ($K_{\text{venue}} = 500$).
9. `comp_baseline`: Historical run rate of the competition tier.
10. `home_pre_match_elo`: Home team Elo rating before match ($K_{\text{elo}} = 32$).
11. `away_pre_match_elo`: Away team Elo rating before match.
12. `batting_order`: Nominal batting position ($1$ to $11$).
13. `batter_balls_faced_before`: Settledness/innings balls faced by current batter.

### 3.3 Secondary Sensitivity: Specification A
Specification A adds `runs_last_12_balls` and `wickets_last_12_balls` to $\mathbf{X}(t^-)$. It is tracked in parallel to confirm robustness across model specifications.

---

## 4. Layer 3: Execution Layer (Value Added)

### 4.1 Responsibilities
The Execution Layer computes the marginal performance of the active players relative to the expectation baseline established in Layer 2.

### 4.2 Batter Execution Metrics
- **Run Value Added (RVA):** $\text{RVA}(t) = \text{ActualRuns}(t) - \hat{\mu}_{\text{runs}}(t^-)$
- **Boundary Execution:** $\text{BGV}(t) = \mathbb{I}(\text{Runs}(t) \in \{4, 6\}) - \hat{P}_{\text{boundary}}(t^-)$
- **Dot Avoidance:** $\text{DAV}(t) = (1 - \mathbb{I}(\text{Runs}(t) = 0)) - (1 - \hat{P}_{\text{dot}}(t^-))$
- **Strike Rotation Rate:** Fraction of non-boundary deliveries yielding 1 or 2 runs.

### 4.3 Bowler Execution Metrics
- **Runs Conceded Suppression (RCS):** $\text{RCS}(t) = \hat{\mu}_{\text{runs}}(t^-) - \text{RunsConceded}(t)$
- **Boundary Prevention:** $\text{BPV}(t) = \hat{P}_{\text{boundary}}(t^-) - \mathbb{I}(\text{RunsConceded}(t) \in \{4, 6\})$
- **Dot Creation:** $\text{DCV}(t) = \mathbb{I}(\text{RunsConceded}(t) = 0) - \hat{P}_{\text{dot}}(t^-)$
- **Wicket Execution:** $\text{WGV}(t) = \mathbb{I}(\text{BowlerWicket}(t) = 1) - \hat{P}_{\text{wicket}}(t^-)$

---

## 5. Layer 4: Reliability, Downside, Consistency & Clutch Layer

### 5.1 Sub-layer 4A: Downside Risk
Reliability is not merely high upside; it is the **bounded probability of catastrophic failure**:
- **Batter Early Dismissal Rate ($\text{EDR}$):**
  $$\text{EDR}_i = \frac{\sum_{m} \mathbb{I}(\text{Dismissed in Match } m \land \text{BallsFaced} \le 5)}{\text{InningsBatted}_i}$$
- **Batter Pressure Collapse Rate ($\text{PCR}$):**
  $$\text{PCR}_i = \frac{\sum_{m} \mathbb{I}(\text{Dismissed in Match } m \land \text{RunsScored} \le 5 \land \text{PressureMean} \ge 0.50)}{\text{InningsBattedUnderPressure}_i}$$
- **Bowler Blowout Over Rate ($\text{BOR}$):**
  $$\text{BOR}_j = \frac{\sum_{o} \mathbb{I}(\text{RunsConceded in Over } o \ge 15)}{\text{OversBowled}_j}$$
- **Bowler Pressure Blowout Rate ($\text{PBOR}$):**
  $$\text{PBOR}_j = \frac{\sum_{o} \mathbb{I}(\text{RunsConceded} \ge 15 \land \text{OverPressureMean} \ge 0.50)}{\text{PressureOversBowled}_j}$$

### 5.2 Sub-layer 4B: Consistency & Dispersion
Measures the predictability of player performance across independent matches:
- **Median Absolute Deviation (MAD):**
  $$\text{MAD}_i = \text{median}\left(\left| \text{VA}_{i,m} - \text{median}(\text{VA}_{i}) \right|\right)$$
- **Interquartile Range (IQR):**
  $$\text{IQR}_i = Q_{0.75}(\text{VA}_{i,m}) - Q_{0.25}(\text{VA}_{i,m})$$
- **Negative Contribution Match Rate:** Fraction of matches where player's cumulative Value Added is negative.

### 5.3 Sub-layer 4C: Clutch / Pressure Delta
Measures whether a player elevates, maintains, or degrades their execution when transitioning from low/medium pressure to acute pressure:
$$\Delta_{\text{clutch}} = \overline{\text{VA}}_{\text{high\_pressure}} - \overline{\text{VA}}_{\text{baseline}}$$
*Critical Confounding Control:* $\overline{\text{VA}}_{\text{baseline}}$ is matched on match phase (Death vs. Middle vs. Powerplay) and bowling type (Pace vs. Spin) to prevent role-composition artifacts from being mistaken for clutch ability.

---

## 6. Layer 5: Evidence & Uncertainty Layer

### 6.1 Empirical Bayes Shrinkage
To account for finite sample sizes without discarding emerging talent, we apply Empirical Bayes shrinkage toward the population mean:
$$\hat{\theta}_i^{\text{EB}} = w_i \cdot \hat{\theta}_i + (1 - w_i) \cdot \mu_0$$
where:
- $\hat{\theta}_i$: Observed sample mean Value Added per delivery under pressure.
- $\mu_0 = 0.0$: Prior population mean Value Added per delivery.
- $w_i = \frac{N_i^*}{N_i^* + K}$: Shrinkage weight, with frozen shrinkage parameter $K = 100$ effective deliveries.

### 6.2 Lower Credible Bound (LCB) Formulation
To guard against sparse-sample variance, decisions evaluate the conservative lower confidence bound:
$$\text{LCB}_{\alpha, i} = \hat{\theta}_i^{\text{EB}} - z_{\alpha} \cdot \text{SE}_i^{\text{EB}}$$
where $\text{SE}_i^{\text{EB}} = \sqrt{\frac{\hat{\sigma}_i^2}{N_i^* + K} + \frac{K \cdot \sigma_0^2}{(N_i^* + K)^2}}$.

Four LCB bounds are calculated and stored in the evidence vector:
- $\text{LCB}_{10}$ ($z = 1.282$): Highly conservative bound.
- $\text{LCB}_{20}$ ($z = 0.842$): **Provisional primary conservative decision metric.**
- $\text{LCB}_{25}$ ($z = 0.674$): Moderate conservative bound.
- $\text{LCB}_{30}$ ($z = 0.524$): Mild conservative bound.

---

## 7. Layer 6: Context & Sample Tier Layer

### 7.1 Evidence Depth Tiers
Players are categorized into three non-overlapping evidence tiers based on sample size:
- **Tier 1 — Robust Evidence:** $N_{\text{total}} \ge 150 \land N_{\text{press}} \ge 40$. High statistical confidence; eligible for immediate unconstrained role deployment.
- **Tier 2 — Moderate Evidence:** $N_{\text{total}} \ge 50 \land N_{\text{press}} \ge 15$. Moderate confidence; eligible for conditional role matching with higher uncertainty margins.
- **Tier 3 — Sparse Evidence:** $N_{\text{total}} < 50 \lor N_{\text{press}} < 15$. High posterior shrinkage; candidate for development or secondary scouting tracking.

### 7.2 Contextual Descriptors
- **Phase Specialization:** $\% \text{Powerplay}, \% \text{Middle}, \% \text{Death}$.
- **Bowling Facing/Type:** $\% \text{vs. Pace}, \% \text{vs. Spin}$.
- **Opposition Difficulty Faced:** Mean opponent Elo rating across faced deliveries.
- **Super Over Annotations:** Qualitative record of Super Over appearances and outcomes.

---

## 8. Layer 7: Decision Interface Layer

The Decision Interface Layer governs how downstream consumers (Stage 4.1 selection workflows) interact with the uncollapsed evidence vector. 

### 8.1 Governance Invariants
1. **No Automatic Collapse:** Layer 7 does NOT produce a singular score.
2. **Modular Inspection:** Any downstream aggregator must report the full profile across all 7 layers.
3. **Traceability:** Every decision must be traceable back to delivery-level telemetry.

*Document Approved by PinkOps Quantitative Governance Committee.*
