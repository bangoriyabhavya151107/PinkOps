# PinkOps — Stage 3.1: Data Leakage Provenance & Verification Audit
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Output Data Reference**: [`data/processed/stage_3_1_feature_provenance.csv`](file:///D:/PinkOps/data/processed/stage_3_1_feature_provenance.csv)  
**Dataset Reference**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) (200,999 deliveries, 867 matches)  

---

## 1. Revised Executive Leakage Statement

In Stage 3.0, the preliminary summary contained the claim: *"ZERO DATA LEAKAGE DETECTED"*. Under independent methodological review, this claim was identified as overly sweeping.

In strict compliance with Stage 3.1 governance, **that claim is hereby revised and replaced with the following formal statement**:

> **"No direct delivery-level temporal leakage was detected in the audited feature construction. Remaining model-level leakage risks involving historical baselines, opponent strength, matchup features, venue/competition estimates, and training-fold construction were separately audited or remain explicitly subject to verification."**

---

## 2. Feature Provenance Registry

Every feature utilized in Stage 3.1 expectation, pressure, and validation models is cataloged below with its complete causal provenance:

| Feature Name | Allowed Timestamp | Allowed Source Data | Current Delivery Allowed? | Future Deliveries Allowed? | Future Matches Allowed? | Match Outcome Allowed? | Training-Fold Restriction | Leakage Status | Verification Assertion |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :--- |
| `innings_progress_before` | $t^-$ | Prior legal balls bowled in innings | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | $B_{\text{bowled}} < B_{\text{total}}$ |
| `balls_remaining_before` | $t^-$ | Scheduled balls minus prior balls | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | $B_{\text{rem}} \ge 0$ |
| `wickets_in_hand_before` | $t^-$ | 10 minus prior innings dismissals | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | $W_{\text{after}} = W_{\text{before}} + W_{\text{ball}}$ |
| `runs_required_before` | $t^-$ | Locked target minus prior runs | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | $R_{\text{after}} = R_{\text{before}} + R_{\text{ball}}$ |
| `target_proximity` | $t^-$ | Ratio of pre-delivery runs to balls | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | Proximity $\ge 0$ |
| `resource_depletion_index` | $t^-$ | Function of prior wickets & progress | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | Bounded in $[0, 18.2]$ |
| `trajectory_deficit` | $t^-$ | Par model prediction minus prior runs | **NO** | **NO** | **NO** | **NO** | Out-of-fold match-grouped model | **LEAKAGE-FREE** | Out-of-fold CV |
| `recent_runs_12` | $t^-$ | Preceding 12 balls (window frame: 12 prec to 1 prec) | **NO** | **NO** | **NO** | **NO** | Match-grouped partition | **LEAKAGE-FREE** | Zero on ball 1 of innings |
| `team_pre_match_elo` | $t^-_{\text{match}}$ | Match results strictly on date $d < D$ | **NO** | **NO** | **NO** | **NO** | Online chronological updating | **LEAKAGE-FREE** | Post-match updates only |
| `venue_shrunk_baseline` | $t^-_{\text{hist}}$ | Out-of-fold/historical venue balls | **NO** | **NO** | **NO** | **NO** | Match-grouped / Prior season | **LEAKAGE-FREE** | EB shrinkage $K=500$ |
| `runs_on_delivery` | $t^+$ | Current delivery outcome | **TARGET ONLY** | **NO** | **NO** | **NO** | Regression Target $Y$ | **TARGET** | Never in feature matrix |
| `is_wicket` | $t^+$ | Current delivery dismissal | **TARGET ONLY** | **NO** | **NO** | **NO** | Classification Target $Y$ | **TARGET** | Never in feature matrix |
| `post_match_winner_team_id`| $T_{\text{final}}$| Final match result | **NO** | **NO** | **NO** | **TRAIN LABEL ONLY**| Win Prob model label | **POST-MATCH**| Quarantined from ball state |

---

## 3. Active Assertion Test Results

The modular pipeline [`src/stage_3_1/leakage_provenance.py`](file:///D:/PinkOps/src/stage_3_1/leakage_provenance.py) executes four executable programmatic assertions across all 200,999 delivery rows:

### Assertion 1: Cumulative Monotonicity Invariant
$$\text{runs\_after} - (\text{runs\_before} + \text{runs\_on\_delivery}) == 0$$
$$\text{wickets\_after} - (\text{wickets\_before} + \text{is\_team\_wicket}) == 0$$
- **Test Result**: **PASS** (0 mismatches across 200,999 deliveries). Pre-delivery state has zero foreknowledge of current delivery runs or wickets.

### Assertion 2: Rolling Window Frame Causal Separation
On ball 1 of every innings (`innings_ball_num == 1`), `recent_runs_12` must be exactly 0.0, even if ball 1 results in a boundary or wicket.
- **Test Result**: **PASS** (0 non-zero values across 1,724 distinct innings).

### Assertion 3: Chronological Online Elo Updating
Elo ratings for match $m$ on date $D_m$ must use only matches played on dates $d < D_m$. Rating updates occur strictly post-match conclusion.
- **Test Result**: **PASS** (867 distinct matches rated in strict temporal order).

### Assertion 4: Complete Target Variable Quarantine
Verify that `runs_on_delivery`, `is_wicket`, `is_four`, `is_six`, and `post_` columns are absent from the expectation feature matrix $\mathbf{X}$.
- **Test Result**: **PASS** (Feature vectors contain strictly pre-delivery covariates).

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
