# PinkOps — Stage 6: Methodological Limitations & Epistemic Honesty Statement
**Project:** Operation Pink Panther / PinkOps  
**Stage:** Stage 6 Final Competition Delivery  
**Document ID:** `outputs/stage_6_limitations.md`  
**Date:** November 2026  

---

## 1. Principles of Epistemic Honesty

A sports analytics framework that claims perfection is fraudulent. In compliance with the PinkOps Analysis Constitution, we transparently document the structural boundaries of our model:

1. **Observational vs. Causal Nature of Clutch Performance:**
   Our matched clutch contrast ($\Delta_{\text{RVA}}$) evaluates empirical performance differentials across matched game situations. Because each delivery is observed in only one state, this represents observational evidence, not proof of counterfactual causal mechanisms.

2. **Unobserved Confounding Variables:**
   Raw ball-by-ball competition records lack data on fielding runs saved, dropped catches, dew intensity, wind velocity, and pitch moisture deterioration. These unobserved factors introduce residual variance.

3. **Captaincy & Tactical Selection Bias:**
   Death-overs bowling is not assigned randomly; elite captains selectively deploy premier bowlers (like Bumrah or Narine) in crisis situations while shielding vulnerable fifth bowlers. Our models adjust for game state, but captaincy acumen remains an unobserved confounder.

4. **Sample Size Sparsity in Emerging Prospects:**
   57.7% of players in the competition dataset reside in the Low / Sparse Evidence tier (< 50 balls). While Empirical Bayes shrinkage appropriately attenuates small samples, high-potential emerging talents with fewer than 50 balls cannot be promoted to Tier 1 core candidates.

5. **No Universal Guarantees in LUB20:**
   LUB20 is derived under conjugate normal-normal assumptions. While Monte Carlo truth testing confirmed ~80% coverage across tested synthetic distributions, it does not provide an unconditional guarantee across non-Gaussian real-world outliers.

6. **Zero Monetary Market Modeling:**
   Because the official Round 1 problem statement omitted auction purse limits and bidding rules, PinkOps does not simulate monetary auction dynamics. Our auction strategy is strictly qualitative and decision-theoretic.

---

*End of Limitations & Epistemic Honesty Statement.*
