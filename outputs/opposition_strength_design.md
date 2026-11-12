# PinkOps — Stage 3.0: Opposition Strength Methodology Design
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Output Data Reference**: [`data/processed/team_pre_match_elo.csv`](file:///D:/PinkOps/data/processed/team_pre_match_elo.csv)  
**Dataset Reference**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet)  

---

## 1. Executive Mandate & Analytical Philosophy

A fundamental challenge in sports analytics is the **Opposition Bias**:
- A batter scoring 35 off 18 against Jasprit Bumrah and Jofra Archer in the IPL death overs has accomplished a vastly more difficult feat than a batter scoring 45 off 18 against an inexperienced bowling attack in a regional associate tournament.
- Conversely, a bowler defending 10 off the final over against Heinrich Klaasen and Nicholas Pooran faces far greater difficulty than defending 10 against a lower-order tailender.

**Strict Governance Directives**:
1. **No Manual League Ratings**: We strictly forbid subjective tiering (e.g., arbitrarily defining "IPL = Tier 1, T20I = Tier 2, Associate = Tier 3").
2. **Zero Circular Data Leakage**: Strength estimates must be derived exclusively from past performance. A match result on May 20, 2024 must NEVER influence the rating assigned to a team or player on May 10, 2024.
3. **Continuous Empirical Estimation**: Strength must be quantified on a continuous, probabilistically calibrated scale.

---

## 2. Comparison of Candidate Methodologies

We evaluate five distinct architectural approaches to estimating opposition strength:

| Dimension | 1. Manual Tiering / Fixed Points | 2. Bradley-Terry / Elo System | 3. Context-Adjusted Ridge Models | 4. Iterative Player-Team Bilinear | 5. Hierarchical Bayesian (MCMC) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mathematical Basis** | Subjective assignment | Pairwise logistic win expectancy | Regularized fixed effects ($L_2$) | Matrix factorization / PageRank | Random-effects prior shrinkage |
| **Data Requirements** | None (Rule-based) | Match results & dates | Delivery telemetry & context | Large dense interaction matrix | Intensive sampling chains |
| **Temporal Integrity** | Static (Time-blind) | **Strict Online Updating ($t^-$)** | Batch retraining required | Batch retraining required | Complex dynamic updates |
| **Computational Cost** | $O(1)$ | $O(M)$ (Instantaneous) | $O(N \cdot P^2)$ (Fast) | $O(\text{iter} \cdot N \cdot K)$ (Moderate) | $O(\text{samples} \cdot N)$ (Very Slow) |
| **Interpretability** | Arbitrary | Intuitive (e.g., 1500 base) | Linear coefficients | Latent embeddings | Full posterior distributions |
| **Leakage Risk** | Low (but biased) | **Zero (Causal online updates)** | High if not time-split | High if not strictly filtered | High across temporal splits |
| **Recommendation** | **REJECTED (Subjective)** | **PRIMARY TEAM FRAMEWORK** | **SECONDARY DELIVERY ADJ** | Exploratory | Rejected (Over-complex) |

---

## 3. Recommended Primary Framework: Dynamic Pre-Match Elo

### Mathematical Formulation
Let each team $i$ possess an Elo rating $R_i(t) \in \mathbb{R}$, initialized to $R_0 = 1500.0$.
Matches $m = 1, \dots, M$ are processed in **strict chronological order** by `(match_date, match_id)`.

Immediately prior to match $m$ between Team $A$ and Team $B$, the pre-match win expectancy for Team $A$ is:
$$\mathbb{P}(\text{Win}_A \mid R_A(t^-), R_B(t^-)) = \frac{1}{1 + 10^{(R_B(t^-) - R_A(t^-))/400}}$$

The pre-match rating differential $\Delta R = R_A(t^-) - R_B(t^-)$ serves as the **unbiased opposition strength covariate** for all deliveries bowled within match $m$.

### Post-Match Rating Update Protocol
Ratings update **strictly after** the match concludes:
$$R_A(t^+) = R_A(t^-) + K \cdot \left(S_A - \mathbb{P}(\text{Win}_A)\right)$$
$$R_B(t^+) = R_B(t^-) + K \cdot \left(S_B - \mathbb{P}(\text{Win}_B)\right)$$

Where:
- $S_A = 1.0$ if Team $A$ wins in normal play or Super Over.
- $S_A = 0.0$ if Team $B$ wins.
- $S_A = 0.5$ if the match ends in a genuine Tie (without Super Over).
- If a match is Abandoned or No-Result, **no rating update occurs** ($S_A = \mathbb{P}(\text{Win}_A) \implies \Delta R = 0$).
- Volatility parameter: $K = 32.0$ (standard T20 responsiveness factor).

### Empirical Validation on Audited Dataset
The pre-match Elo engine was executed across all 867 contested matches in the dataset (2022 to 2026). The resulting ratings naturally and organically separated elite international and franchise powerhouses from developing associate programs:

**Top 10 Teams by Dynamic Pre-Match Elo**:
1. **England** ($1715.0$)
2. **Australia** ($1649.8$)
3. **India** ($1632.4$)
4. **Royal Challengers Bengaluru** ($1616.8$)
5. **Pakistan** ($1612.9$)
6. **Pakistan A** ($1567.4$)
7. **Gujarat Titans** ($1557.3$)
8. **Afghanistan A** ($1553.8$)
9. **Sunrisers Hyderabad** ($1539.0$)
10. **New Zealand** ($1534.5$)

**Bottom 10 Teams by Dynamic Pre-Match Elo**:
- **United Arab Emirates** ($1346.6$)
- **Oman** ($1408.8$)
- **Hong Kong** ($1416.8$)
- **Zimbabwe** ($1316.2$)

This separation emerged **entirely from 867 match outcomes**, without a single human-assigned weight or subjective tier!

---

## 4. Delivery-Level Opponent Attack Adjustment

While team Elo captures institutional strength, T20 matches are contested at the individual batter vs. bowler level. Within the same team, facing an elite spearhead is distinct from facing a part-time sixth bowler.

### Causal Historical Attack Profiling
For every delivery $t$, the opposing bowler or batter is evaluated based on their **pre-match historical track record**:
1. **Opponent Bowler Difficulty ($\Omega_{\text{bowler}}$)**:
   $$\Omega_{\text{bowler}}(t^-) = \omega_{\text{econ}} \cdot \left(\overline{\text{Econ}}_{\text{global}} - \text{Econ}_{\text{bowler, hist}}\right) + \omega_{\text{dot}} \cdot \text{DotRate}_{\text{bowler, hist}} + \omega_{\text{wkt}} \cdot \text{WktRate}_{\text{bowler, hist}}$$
2. **Opponent Batter Threat ($\Omega_{\text{batter}}$)**:
   $$\Omega_{\text{batter}}(t^-) = \beta_{\text{sr}} \cdot \left(\text{SR}_{\text{batter, hist}} - \overline{\text{SR}}_{\text{global}}\right) + \beta_{\text{bound}} \cdot \text{BoundaryRate}_{\text{batter, hist}}$$

### Empirical Bayes Shrinkage for Low-Sample Players
To prevent small-sample players (e.g., a debutant bowler with 12 balls) from receiving extreme difficulty ratings, all player statistics are shrunk toward the population prior:
$$\hat{\theta}_{\text{player, hist}} = \frac{N_{\text{prior\_balls}}}{N_{\text{prior\_balls}} + K_{\text{player}}} \bar{x}_{\text{observed}} + \frac{K_{\text{player}}}{N_{\text{prior\_balls}} + K_{\text{player}}} \mu_{\text{global}}$$
where $K_{\text{player}} = 120$ balls (equivalent to ~5 full T20 matches).

---

## 5. Strict Leakage Controls & Governance

To ensure referential and temporal integrity:

### 1. Temporal Ordering Invariant
A match played on date $D$ can only utilize ratings derived from matches played on dates $d < D$. If two matches occur on the same date, they are ordered deterministically by `match_id`.

### 2. Treatment of New Teams and Debutants
- A new team entering the dataset starts exactly at the prior mean ($R_0 = 1500.0$).
- A debutant player entering their first match has $N_{\text{prior\_balls}} = 0$, meaning their historical attack rating shrinks 100% to $\mu_{\text{global}}$ (zero artificial penalty or bonus).

### 3. Cross-Competition Bridges
Because international teams (e.g., India, Australia) and franchise teams (e.g., RCB, GT) do not play directly against each other, their Elo pools operate in interconnected subgraphs bridged by player rosters and tournament structures. In Stage 3, team Elo differences are applied **within-competition** ($\Delta R = R_{\text{home}} - R_{\text{away}}$), ensuring that the rating differential is always internally consistent and normalized.

---

## 6. Implementation Architecture in Stage 3 Code

The reproducible pipeline [`src/03_pressure_discovery.py`](file:///D:/PinkOps/src/03_pressure_discovery.py) implements:
1. Dynamic chronological Elo rating simulation.
2. Production of [`data/processed/team_pre_match_elo.csv`](file:///D:/PinkOps/data/processed/team_pre_match_elo.csv) mapped to all 867 matches.
3. Inner join of `home_pre_match_elo`, `away_pre_match_elo`, and `elo_diff_home_minus_away` into the delivery feature matrix.
4. Active assertion checks confirming that pre-match ratings strictly precede match completion.

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
