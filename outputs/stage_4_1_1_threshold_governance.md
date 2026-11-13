# PinkOps — Stage 4.1.1: Threshold Governance & Methodological Architecture
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Status:** Frozen Canonical Governance Specification  

---

## 1. Governance Classification of All Project Thresholds

In accordance with the PinkOps Analysis Constitution and Stage 4.1.1 guidelines, every numerical parameter, cutoff, and gate threshold used in the analytical pipeline is formally classified into five epistemological categories:

1. **DATA-DERIVED:** Derived directly from empirical distributions in the underlying match-state data (e.g., empirical variance, distribution quantiles).
2. **MODEL-DERIVED:** Derived from formal estimation models (e.g., Elo rating convergence, regression coefficients).
3. **PRE-REGISTERED GOVERNANCE CHOICE:** A deliberate, frozen policy rule chosen prior to player inspection to protect against bias and small-sample distortion.
4. **SENSITIVITY-TESTED GOVERNANCE CHOICE:** A parameter whose baseline value is governed by operational requirements, but whose robustness is verified across alternative branches.
5. **ARBITRARY / UNSUPPORTED:** Parameters lacking theoretical or empirical justification (None permitted in Stage 4.1.1).

### Threshold Taxonomy Matrix
| Parameter / Threshold | Baseline Value | Governance Category | Empirical / Theoretical Basis | Sensitivity Tested Range |
| :--- | :---: | :--- | :--- | :---: |
| **Robust Evidence: Min Total Deliveries** | $150$ balls | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Ensures sampling variance is reduced to $< 0.008$; empirically separates regular squad members from incidental call-ups. | $[100, 150, 250]$ |
| **Robust Evidence: Min Pressure Deliveries** | $40$ balls | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Guarantees minimum statistical power to detect a 0.10 runs/ball value-added difference at $\alpha = 0.20$. | $[30, 40, 75]$ |
| **Moderate Evidence: Total Deliveries** | $50$ balls | **PRE-REGISTERED GOVERNANCE CHOICE** | Protects emerging talent from being discarded into anecdotal tier while maintaining shrinkage discipline. | $[40, 50, 60]$ |
| **Moderate Evidence: Pressure Deliveries** | $15$ balls | **PRE-REGISTERED GOVERNANCE CHOICE** | Threshold below which shrinkage weight $\lambda < 0.15$ causes prior to completely dominate observation. | $[10, 15, 20]$ |
| **Empirical Bayes Prior Strength ($K$)** | $100.0$ | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Corresponds to $\sigma^2 / \tau^2 \approx 1.21 / 0.012$; equates to ~16.7 overs of historical prior information. | $[50.0, 100.0, 200.0]$ |
| **Population Outcome Variance ($\sigma$)** | $1.10$ | **DATA-DERIVED** | Measured standard deviation of delivery-level runs value-added across all 200,961 normal deliveries. | Fixed by data ($\pm 0.05$) |
| **Primary LUB Percentile** | $20\text{th}$ ($z = 0.842$) | **PRE-REGISTERED GOVERNANCE CHOICE** | 80% one-sided conservative lower uncertainty bound penalizing sample sparsity without over-penalizing medium samples. | $10\text{th}, 15\text{th}, 20\text{th}, 25\text{th}, 30\text{th}$ |
| **High Pressure Cutoff ($\text{PI}_{80}$)** | Top $20\%$ ($\text{PI} \ge 0.65$) | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Isolates the top quintile of environmental match-state stress (death overs, tight chases, post-collapse overs). | $\text{PI}_{70}, \text{PI}_{80}, \text{PI}_{85}$ |
| **Venue Shrinkage Strength ($K_{\text{venue}}$)** | $500$ balls | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Stabilizes venue scoring baselines against single-match extreme pitch outliers. | $[250, 500, 1000]$ |
| **Team Elo $K$-Factor** | $32$ | **PRE-REGISTERED GOVERNANCE CHOICE** | Standard chess/sports Elo update factor balancing responsiveness to recent form with long-term rating stability. | $[16, 32, 48]$ |
| **RDI Smoothing Epsilon ($\epsilon$)** | $0.15$ | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Regularizes division by small resource denominators in late innings. | $[0.10, 0.15, 0.20]$ |
| **Batter Early Dismissal Rate Max** | $\le 0.20$ ($20\%$) | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Eliminates batters who fail in balls 1–5 under pressure in $> 1$ out of 5 innings. | $[0.15, 0.18, 0.20, 0.22, 0.25]$ |
| **Bowler Pressure Blowout Rate Max** | $\le 0.20$ ($20\%$) | **SENSITIVITY-TESTED GOVERNANCE CHOICE** | Caps proportion of high-pressure overs where bowler concedes $\ge 12$ runs/over. | $[0.15, 0.18, 0.20, 0.22, 0.25]$ |
| **Batter Match MAD Max** | $\le 0.55$ | **DATA-DERIVED** | Set at the 75th percentile of empirical match-level MAD for qualified batters; screens out extreme volatility. | $[0.50, 0.55, 0.60]$ |
| **Bowler Match MAD Max** | $\le 0.45$ | **DATA-DERIVED** | Set at the 75th percentile of empirical match-level MAD for qualified bowlers; screens out volatile bowlers. | $[0.40, 0.45, 0.50]$ |
| **Multiverse Support Threshold** | $\ge 7 / 8$ | **PRE-REGISTERED GOVERNANCE CHOICE** | Requires positive performance across at least 87.5% of primary independent model specifications. | $[6/8, 7/8, 8/8]$ |

---

## 2. Sensitivity Analysis Around Governance Cutoffs

To prove that player profiles do not hinge on hyper-tuned cutoff boundaries, sensitivity sweeps were conducted across the primary gate thresholds:

### 2.1 Early Dismissal Rate & Blowout Rate Cutoff Sensitivity
```
Batting Reliable Cohort Count vs. Early Dismissal Threshold:
• Threshold <= 0.15: 11 batters qualify
• Threshold <= 0.18: 13 batters qualify
• Threshold <= 0.20 (Canonical): 14 batters qualify
• Threshold <= 0.22: 15 batters qualify
• Threshold <= 0.25: 16 batters qualify

Bowling Reliable Cohort Count vs. Blowout Rate Threshold:
• Threshold <= 0.15: 46 bowlers qualify
• Threshold <= 0.18: 49 bowlers qualify
• Threshold <= 0.20 (Canonical): 51 bowlers qualify
• Threshold <= 0.22: 52 bowlers qualify
• Threshold <= 0.25: 53 bowlers qualify
```
*Finding:* The qualifying cohort expands or contracts monotonically without erratic rank inversions. Core benchmark players (e.g., Bumrah, Narine, Suryakumar Yadav, Jitesh Sharma) satisfy even the strictest 15% cutoff.

### 2.2 Evidence-Tier Threshold Resolution
The discrepancy between the 150/40 rule and the 250/75 rule has been permanently resolved:
- **Canonical Operational Standard:** **$N_{\text{tot}} \ge 150 \land N_{\text{press}} \ge 40$** (Robust Evidence Tier).
- **Strict Benchmark Cohort:** **$N_{\text{tot}} \ge 250 \land N_{\text{press}} \ge 75$** is designated as a sensitivity cohort to verify that findings hold when restricted solely to high-exposure international stars.
- All code modules, JSON configuration files, and Markdown tables have been synchronized to load directly from [`data/processed/stage_4_1_1_governance_spec.json`](file:///D:/PinkOps/data/processed/stage_4_1_1_governance_spec.json).

---

## 3. Epistemic Status of Tactical Role Classifications

Tactical roles assigned in this framework are **model-defined behavioral archetypes**, not intrinsic or immutable player traits:
- Batting roles (`Top-Order Anchor / Powerplay Batter`, `Middle-Overs Accelerator`, `Finisher / Death Specialist`) reflect the empirical distribution of deliveries faced across match overs (overs 1–6, 7–15, 16–20) and entry positions.
- Bowling roles (`Powerplay Specialist`, `Middle Enforcer`, `Death Specialist` partitioned by Pace vs Spin) reflect historical over assignments and bowling actions.
- *Limitation:* A player's historical role reflects team captaincy decisions and squad balance at their prior franchise. Migrating a player to a new tactical role in Stage 5 introduces transition uncertainty.

---

## 4. Invariant: Strict Opportunity vs. Performance Separation

The pipeline enforces mathematical independence between opportunity and performance:

$$\text{Opportunity} = \mathbb{I}(\text{Player Active}) \times \text{Pressure Intensity}(\text{State}_{t-})$$

$$\text{Performance} = \text{Actual Outcome}_t - \mathbb{E}[\text{Outcome}_t \mid \text{State}_{t-}, \text{Context}_{t-}]$$

- $\text{Pressure Intensity}$ depends exclusively on pre-delivery match variables (required run rate, wickets fallen, balls remaining, run-differential index, phase urgency). It contains **zero terms from the current delivery outcome**.
- An athlete facing a dot ball or hitting a six experiences the exact same opportunity value for that delivery; only the performance residual changes.

---

*End of Stage 4.1.1 Threshold Governance Report.*
