# PinkOps — Stage 4.1.1: Comprehensive Player Attribution & Ledger Reconciliation Audit
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Verification Script:** `src/stage_4_1_1/attribution_audit.py`  
**Dataset Artifact:** [`data/processed/stage_4_1_1_attribution_audit.csv`](file:///D:/PinkOps/data/processed/stage_4_1_1_attribution_audit.csv)  
**Date:** November 2026  

---

## 1. Executive Summary & Attribution Governance

In competitive sports analytics, assigning outcomes to the wrong actor produces severe selection distortion. Naive counting statistics often charge byes and leg-byes to bowlers, credit extras to batters, or penalize batters for run-outs where the non-striker or fielder was responsible.

This audit establishes the **zero-leakage attribution accounting ledger** reconciling all **200,999 raw competition deliveries** across both the canonical modeling population (200,961 normal-innings balls) and the isolated Super Over register (38 balls).

---

## 2. Extras Attribution Accounting Ledger

The table below reconciles all extras types observed in the dataset and states their formal assignment rules:

| Extra Type | Raw Delivery Count | Normal Delivery Count | Super Over Count | Batter Faced Ball? | Batter Credited Runs? | Bowler Charged Conceded Runs? | Methodological & Scoring Accounting Rule |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Clean Delivery (No Extras)** | 189,167 | 189,132 | 35 | **Yes (1)** | **Yes (Runs off bat)** | **Yes (Runs off bat)** | Standard legal delivery. Batter execution credited; bowler conceded runs charged. |
| **Wide** | 7,714 | 7,713 | 1 | **No (0)** | **No (0)** | **Yes (Extras + runs)** | Bowler execution error. Batter did not face a legal ball; excluded from batter balls faced denominator. |
| **Leg Byes** | 2,748 | 2,748 | 0 | **Yes (1)** | **No (0)** | **No (0)** | Fielding extra off batter's pad/body. Batter faced delivery; strictly excluded from bowler conceded runs. |
| **No Balls (Overstep)** | 576 | 575 | 1 | **Yes (1)** | **Yes (Runs off bat)** | **Yes (Penalty + bat)** | Bowler illegal delivery. Batter faced ball; penalty run charged to bowler ledger. |
| **Byes** | 529 | 528 | 1 | **Yes (1)** | **No (0)** | **No (0)** | Wicketkeeper extra. Batter faced delivery; strictly excluded from bowler conceded runs. |
| **Other Illegal Deliveries** | 264 | 264 | 0 | **Yes (1)** | **Yes (Runs off bat)** | **Yes (Penalty + bat)** | Height/beam illegal deliveries; extra charged to bowler ledger. |
| **Penalty Runs** | 1 | 1 | 0 | **No (0)** | **No (0)** | **No (0)** | Team conduct penalty awarded by umpires; isolated from individual player metrics. |
| **Total Deliveries** | **200,999** | **200,961** | **38** | — | — | — | Full delivery universe accounted for without omission. |

---

## 3. Dismissal Attribution & Downside Accounting

The table below reconciles all dismissals recorded across normal-innings modeling:

| Dismissal Type | Raw Count | Normal Count | Super Over Count | Bowler Wicket Credited? | Batter Dismissal Charged? | Downside Metric Impact & Isolation Policy |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Caught** | 7,557 | 7,556 | 1 | **Yes (1)** | **Yes (1)** | Direct execution dismissal. Batter charged with dismissal; bowler credited with wicket. |
| **Bowled** | 1,775 | 1,774 | 1 | **Yes (1)** | **Yes (1)** | Direct execution dismissal. Clean bowled; bowler credited with wicket. |
| **LBW** | 709 | 709 | 0 | **Yes (1)** | **Yes (1)** | Direct execution dismissal. Leg before wicket; bowler credited with wicket. |
| **Run Out** | 600 | 598 | 2 | **No (0)** | **Isolated (0)** | Team dismissal. Involves non-striker call, running communication, and fielder direct hit. Strictly 0 bowler wickets; isolated from batter execution failure. |
| **Stumped** | 214 | 214 | 0 | **Yes (1)** | **Yes (1)** | Direct execution dismissal. Bowler and wicketkeeper credited; batter dismissed. |
| **Hit Wicket** | 17 | 17 | 0 | **Yes (1)** | **Yes (1)** | Direct execution dismissal. Batter error; credited to bowler. |
| **Retire Out** | 6 | 6 | 0 | **No (0)** | **Yes (1)** | Tactical team dismissal. Batter charged with tactical dismissal; 0 bowler wickets. |
| **Obstructing Field** | 3 | 3 | 0 | **No (0)** | **Yes (1)** | Conduct dismissal. Batter charged; 0 bowler wickets. |
| **None (Not Out)** | 190,118 | 190,084 | 34 | **No (0)** | **No (0)** | Delivery did not produce a dismissal. |

---

## 4. Special Handling: Run-Outs and Retired-Hurt Events

### 4.1 Run-Out Isolation Protocol
Across the 200,999 delivery dataset, **600 run-out events occur** (598 in normal-innings modeling, 2 in Super Overs).
- **Bowler Ledger:** Under MCC and ICC playing conditions, bowlers are never credited with wickets on run-outs. **0 bowler wickets are charged or credited.**
- **Batter Ledger:** A run-out cannot be cleanly attributed to the striker versus non-striker without video tracking. Charging a striker with execution failure when the non-striker initiates a suicidal run introduces severe noise. In the Stage 4.1.1 pipeline, run-outs are tracked as team wickets in match state, but are **isolated from individual batter execution value-added ($\text{VA}_{\text{exec}}$) and early dismissal rate ($\text{EDR}$)** unless the striker was definitively run out facing the ball.

### 4.2 Retired Hurt: Complete Injury Isolation
- **12 deliveries in the dataset contain `is_retired_hurt == 1`** (all 12 in normal-innings modeling).
- Every single one has been independently audited and verified:
  - $\sum \text{is\_bowler\_wicket} = 0$
  - $\sum \text{is\_team\_wicket} = 0$
- **Policy Enforcement:** Physical injury is an exogenous medical shock. It is **strictly isolated from batter collapse penalties, early dismissal rates, and bowler wicket credit**.

---

*End of Stage 4.1.1 Attribution Accounting Audit.*
