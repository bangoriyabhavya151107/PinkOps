# PinkOps — Stage 4.0 Remediation: Scientific Language & Epistemic Calibration Audit

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_language_audit.md`  
**Stage:** 4.0 Remediation (Fix 6)  
**Governance Status:** AUDITED & CALIBRATED  

---

## 1. Executive Summary & Calibration Mandate

In competitive quantitative sports research, overclaiming weakens methodology. Mathematical formulations and empirical validations must state what they actually measure, the exact approximations used, and their empirical boundaries without manufacturing artificial certainty.

During the Stage 4.0 audit, several terms were flagged for uncalibrated assertion. This document audits all identified terms across the Stage 4.0 documentation and source code, providing the line-by-line replacement mapping to scientifically disciplined formulations.

---

## 2. Systematic Terminology Replacement Registry

| Prohibited Overclaiming Term | Calibrated Approved Formulation | Methodological Rationale | Affected Documents |
|---|---|---|---|
| *"Zero structural bias in the model"* | *"Role-related confounding was substantially attenuated under the adjusted specification."* | No observational model eliminates all bias; role adjustment reduces confounding. | `stage_4_0_reliability_architecture.md`, `stage_4_0_robustness_governance.md` |
| *"Zero data leakage detected"* | *"No direct delivery-level temporal leakage was detected in the audited feature construction; model-level leakage risks involving historical baselines, opponent strength, matchup features, venue/competition estimates, and training-fold construction were separately reviewed or remain explicitly subject to verification under pre-registered cross-validation protocols."* | Distinguishes delivery-level temporal isolation from cross-fold aggregation risks. | `stage_4_0_leakage_governance.md`, `stage_4_0_reliability_estimand.md` |
| *"Elo ranking order is invariant"* | *"Top-five membership was stable across tested Elo K values (16, 32, 48), while internal ordering changed within the cohort."* | Elo parameter shifts cause minor rank swaps within cohorts, though top membership holds. | `stage_4_0_robustness_governance.md` |
| *"LCB20 confirmed as the singularly correct choice"* | *"LUB20 is a provisional conservative decision metric supported by sensitivity stability."* | Quantile choices represent risk-preference governance decisions, not mathematical absolutes. | `stage_4_0_robustness_governance.md`, `stage_4_0_reliability_architecture.md` |
| *"The pressure score is perfectly objective"* | *"Pressure intensity is an environmental property derived strictly from pre-delivery match telemetry."* | Pressure is an engineered metric derived from match state, not an unassailable physical constant. | `stage_4_0_reliability_estimand.md` |
| *"Bayesian posterior credible interval"* | *"Lower Uncertainty Bound (LUB) under an Empirical Bayes normal-approximation framework."* | A true credible interval requires an explicit Bayesian generative posterior distribution. | `stage_4_0_reliability_architecture.md`, `stage_4_0_player_evidence_schema.md` |
| *"Causal clutch effect / True clutch rating"* | *"Descriptive context-adjusted pressure differential."* | Observational match data cannot establish pure causality due to unobserved conditions. | `stage_4_0_clutch_matching_audit.md`, `stage_4_0_player_evidence_schema.md` |
| *"Mathematically optimal hyperparameters"* | *"Primary operating specifications selected based on robustness and interpretability under the tested sensitivity grid."* | Hyperparameters balance bias and variance; they are robust operating choices. | `stage_4_0_robustness_governance.md`, `stage_4_0_methodology_spec.json` |
| *"Specification B is objectively unbiased"* | *"Specification B reduces endogenous self-conditioning of player attribution while producing negligible predictive loss under the tested validation design."* | Spec B removes recent-12 form absorption, but observational data retains background variance. | `stage_4_0_reliability_estimand.md` |
| *"Guaranteed performance under pressure"* | *"Empirical evidence of consistent historical execution above contextual expectation."* | Statistical evidence quantifies historical repeatability; it cannot guarantee future match outcomes. | `stage_4_0_reliability_architecture.md` |

---

## 3. Core Epistemic Principles for Stage 4.1

Throughout all Stage 4.1 implementations, the following 15 epistemic rules are enforced:
1. **Correlation is not causation:** High Value Added correlates with run-scoring; it does not prove unassisted skill.
2. **Residual performance is not automatically pure skill:** Residuals include unobserved pitch, ball, and tactical noise.
3. **Pressure exposure is not pressure performance:** Encountering high pressure does not mean performing well in it.
4. **High performance with tiny sample size is weak evidence:** 15 balls of $+0.40$ VA is high-variance noise.
5. **High sample size does not automatically imply high reliability:** A 400-ball accumulator can have unacceptable downside collapse rates.
6. **LUB is not the entire reliability construct:** LUB provides an uncertainty floor; it must be viewed alongside downside, consistency, and clutch.
7. **Clutch delta is descriptive:** It is a matched observational contrast, not a randomized trial.
8. **LOCO is a transfer test, not proof of universality:** Generalization across 5 competitions indicates robust league adaptation, not universal invariance.
9. **Sensitivity stability does not prove parameter optimality:** Stability across tested values proves resilience, not perfection.
10. **EB shrinkage reduces variance; it does not remove bias:** Shrinkage pulls toward the prior mean; it does not correct measurement bias.
11. **Role adjustment reduces confounding; it does not prove zero bias:** Role stratifications attenuate phase effects, but subtle role differences remain.
12. **Historical opponent strength must be strictly pre-match:** No post-match outcomes in Elo.
13. **Venue and competition baselines must respect fold isolation:** No target leakage in cross-validation.
14. **Super Overs are separate stress-test evidence:** 38 balls cannot be mixed with regular 20-over curves.
15. **Never manufacture certainty from sparse evidence:** Maintain explicit uncertainty intervals on all player profiles.

*Document Approved by PinkOps Quantitative Governance Committee.*
