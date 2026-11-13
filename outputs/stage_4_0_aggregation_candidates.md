# PinkOps — Stage 4.0: Aggregation Methodology Candidate Evaluation

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_aggregation_candidates.md`  
**Stage:** 4.0 — Reliability Architecture, Estimand Freeze & Governance  
**Governance Status:** CANDIDATE EVALUATION (Zero Premature Winner Selection)  

---

## 1. Executive Summary & Purpose

A critical governance principle of Operation Pink Panther is that **we do NOT collapse the uncollapsed player evidence vector into an arbitrary single score during Stage 4.0**.

However, when Stage 4.1 executes player evaluation, decision-makers will require a principled mechanism to transition from the 33-dimensional evidence vector to actionable franchise decisions (squad selection, role assignment, and auction valuation). 

This document formally defines and evaluates the **five viable mathematical aggregation methodologies**. Each candidate is audited against rigorous axiomatic standards, operational trade-offs, and failure modes. In accordance with the Stage 4.0 charter, **no single method is chosen as the exclusive winner here**; all five candidate specifications are preserved for Stage 4.1 implementation.

---

## 2. Comparative Evaluation Matrix

| Criterion | Method A: Hurdle Gate-and-Rank | Method B: Constrained Multi-Objective | Method C: Lower Credible Bound (LCB) | Method D: Factor / PCA Latent Index | Method E: Explicit Tiered Matrix |
|---|---|---|---|---|---|
| **Mathematical Complexity** | Low (Piecewise boolean + sort) | High (Non-linear optimization) | Medium (Empirical Bayes + normal quantile) | Medium-High (Eigen-decomposition) | Low (Binned multi-criteria classification) |
| **Axiomatic Alignment** | Moderate (Cliff effects at hurdles) | Very High (Pareto optimality guaranteed) | High (Monotone in evidence & performance) | Low-Moderate (Non-invariant sign/rotation) | Moderate (Discrete binning boundaries) |
| **Sample-Size Conservatism** | Explicit via qualification gate | Explicit via constraint set | Mathematically optimal via shrinkage | Weak (PCA variance dominated by outliers) | Explicit via tier membership |
| **Downside Risk Protection** | Strict hard constraint | Strict mathematical constraint | Implicit (via sample variance penalty) | None (Blends positive and negative tails) | Explicit category separation |
| **Franchise Interpretability** | Very High ("Passed all checks, top performer") | Moderate-Low (Complex frontier trade-offs) | High ("Guaranteed 80% confidence floor") | Very Low ("0.42 on Component 1") | Extremely High ("Tier 1 Elite Finisher") |
| **Susceptibility to Overfitting** | Very Low | Low | Very Low | Moderate | Low |
| **Stage 4.0 Recommendation** | **Strong Primary Candidate** | **Recommended for Scenario Frontier** | **Strong Primary Candidate** | **Not Recommended for Decision-Making** | **Strong Operational Complement** |

---

## 3. Detailed Audit of Candidate Methods

### 3.1 Method A: Hurdle / Gate-and-Rank

#### 3.1.1 Mathematical Formulation
Let $\mathcal{P}$ be the set of all players. A player $i \in \mathcal{P}$ qualifies for final ranking if and only if they satisfy four simultaneous boolean hurdles:
$$\mathcal{Q} = \left\{ i \in \mathcal{P} \;\middle|\; \begin{aligned}
N_{i,\text{total}} &\ge N_{\min} \quad (\text{Sample Size Gate}) \\
N_{i,\text{press}} &\ge N_{\min,\text{press}} \quad (\text{Pressure Evidence Gate}) \\
\text{Downside}_i &\le \tau_{\text{down}} \quad (\text{Catastrophe Gate: EDR} \le 0.25 \text{ or BOR} \le 0.20) \\
\text{Consistency}_i &\le \tau_{\text{mad}} \quad (\text{Dispersion Gate: MAD} \le \text{MAD}_{0.80})
\end{aligned} \right\}$$

For all qualified players $i \in \mathcal{Q}$, ranking is determined strictly by the conservative Lower Credible Bound Value Added:
$$\text{Rank}(i) = \text{Order}\left(\theta_i^{\text{LCB20}}\right)$$

#### 3.1.2 Axiomatic Alignment
- **Monotonicity:** Satisfied for qualified players (higher value added strictly improves rank).
- **Scale Invariance:** Satisfied (units remain runs/ball).
- **Independence of Irrelevant Alternatives (IIA):** Partially violated at the qualification threshold (a minor shift in $\tau_{\text{down}}$ can disqualify a borderline player).

#### 3.1.3 Failure Modes & Edge Cases
- **Cliff-Edge Effect:** A batter with an early dismissal rate of $0.251$ is completely disqualified, while a batter with $0.249$ is ranked #1.
- **Remedy:** Use soft-penalty transitions or tiered qualification gates rather than brittle step-functions.

---

### 3.2 Method B: Constrained Multi-Objective Optimization

#### 3.2.1 Mathematical Formulation
Formulate squad selection as a constrained Pareto optimization problem:
$$\max_{w} \sum_{i \in \mathcal{P}} w_i \cdot \theta_i^{\text{EB}}$$
subject to:
$$\begin{aligned}
\sum_{i \in \mathcal{P}} w_i \cdot \text{EDR}_i &\le \gamma_{\text{bat}} \quad (\text{Squad Early Dismissal Cap}) \\
\sum_{j \in \mathcal{P}} w_j \cdot \text{BOR}_j &\le \gamma_{\text{bowl}} \quad (\text{Squad Over Blowout Cap}) \\
\sum_{i \in \mathcal{P}} w_i \cdot \text{SE}_i^{\text{EB}} &\le \Omega \quad (\text{Squad Epistemic Uncertainty Budget}) \\
\sum_{i \in \mathcal{P}} w_i &= K_{\text{squad}}, \quad w_i \in \{0, 1\}
\end{aligned}$$

#### 3.2.2 Axiomatic Alignment
- **Pareto Efficiency:** Guaranteed. No alternative player selection exists that yields higher expected value added without worsening downside risk or uncertainty.
- **Compositional Coherence:** Optimizes the 11-player unit rather than 11 isolated individuals.

#### 3.2.3 Failure Modes & Edge Cases
- **Non-Linear Combinatorics:** Requires integer programming solvers (e.g., HiGHS / GLPK).
- **Indifference Planes:** Does not yield a unique 1-to-N player ranking; only produces optimal sets.

---

### 3.3 Method C: Pure Lower Credible Bound (LCB) Ranking

#### 3.3.1 Mathematical Formulation
Rank all players directly by their conservative lower credible bound:
$$\text{Score}_i = \theta_i^{\text{LCB20}} = \hat{\theta}_i^{\text{EB}} - 0.842 \cdot \text{SE}_i^{\text{EB}}$$
where $\hat{\theta}_i^{\text{EB}}$ represents Empirical Bayes shrinkage ($K = 100$) and $\text{SE}_i^{\text{EB}}$ encapsulates both aleatoric match variance and epistemic sample sparsity.

#### 3.3.2 Axiomatic Alignment
- **Informationally Complete:** Naturally penalizes low sample sizes, high variance, and weak opposition through the standard error expansion without arbitrary threshold cuts.
- **Strict Monotonicity:** Every additional successful delivery strictly increases $\text{Score}_i$.

#### 3.3.3 Failure Modes & Edge Cases
- **Implicit Downside Conflation:** A player who achieves a modest LCB through high consistency and zero boundaries is ranked equivalently to an explosive batter who has higher variance.
- **Remedy:** Must be paired with Layer 4 downside descriptors in executive reporting.

---

### 3.4 Method D: Principal Component / Factor-Based Latent Index

#### 3.4.1 Mathematical Formulation
Apply unsupervised PCA or Exploratory Factor Analysis across the standardized 12 key metrics in Layers 1–5:
$$\mathbf{Z} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$$
Extract the first latent factor $F_1$ (capturing maximum shared variance) as the "Reliability Factor".

#### 3.4.2 Axiomatic Alignment & Disqualification
- **Sign Ambiguity:** Eigenvectors are rotationally invariant up to sign; requires manual orientation.
- **Blends Positive and Negative Failure Modes:** PCA forces orthogonal linear combinations, conflating dot avoidance with boundary hitting.
- **Axiomatic Violation:** Violates scale and unit interpretability. A player's score becomes an abstract z-score unit.
- **Governance Finding:** **Method D is formally rejected as a primary decision aggregator.** It may be retained solely as an unsupervised diagnostic for collinearity.

---

### 3.5 Method E: Explicit Tiered Decision Matrix

#### 3.5.1 Mathematical Formulation
Classify players into discrete, mutually exclusive operational tiers:
- **Tier 1 — Elite High-Leverage Anchors:** $\text{LCB20} > +0.10 \land \text{EDR} \le 0.15 \land \text{Evidence} = \text{Robust}$.
- **Tier 2 — Solid Contextual Contributors:** $\text{LCB20} > +0.00 \land \text{EDR} \le 0.25 \land \text{Evidence} \in \{\text{Robust}, \text{Moderate}\}$.
- **Tier 3 — High-Variance Upside Specialists:** $\hat{\theta}^{\text{EB}} > +0.15 \land \text{MAD} > \text{MAD}_{0.75}$ (High reward, elevated downside).
- **Tier 4 — Unverified / Developmental:** $\text{Evidence} = \text{Sparse}$ (Promising micro-sample, high posterior shrinkage).

#### 3.5.2 Axiomatic Alignment
- **Axiom of Role Specialization:** Reflects real-world squad construction where teams need distinct player profiles (steady death anchors vs. boundary-hitting gambits).
- **Operational Clarity:** Direct alignment with scouting and auction room vernacular.

---

## 4. Governance Decision & Stage 4.1 Implementation Roadmap

1. **Zero Premature Collapse:** No candidate method is executed to generate player rankings in Stage 4.0.
2. **Recommended Architecture for Stage 4.1:** The Quantitative Governance Committee recommends a **hybrid synthesis of Method A (Hurdle Gating), Method C (LCB20 Ordering), and Method E (Tier Categorization)** for Stage 4.1 execution:
   - *Hurdles (Method A)* screen out catastrophe-prone or unverified players.
   - *LCB20 (Method C)* provides the continuous, uncertainty-penalized sorting within qualified cohorts.
   - *Tier Matrix (Method E)* translates the quantitative outputs into tactical role archetypes for Rajasthan Royals decision-makers.

*Document Approved by PinkOps Quantitative Governance Committee.*
