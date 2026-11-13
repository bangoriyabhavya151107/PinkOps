# PinkOps — Stage 4.0 Remediation: Player Attribution Accounting Audit

**Project:** Operation Pink Panther  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Brand:** PinkOps  
**Document ID:** `outputs/stage_4_0_player_attribution_audit.md`  
**Stage:** 4.0 Remediation (Fix 3)  
**Governance Status:** AUDITED & VERIFIED (8/8 Assertions Passed)  

---

## 1. Executive Summary & Purpose

A fundamental failure mode in sports data engineering is assigning events to the wrong actor (e.g. charging a bowler for byes conceded due to a wicketkeeper error, or crediting a batter for leg-byes deflected off the pad). 

The Stage 4.0 audit revealed that the initial prototype used raw `runs_on_delivery` as the outcome variable for both batters and bowlers. In standard cricket laws:
- **Batters** score runs off the bat only. Byes, leg-byes, wides, and penalty runs are team extras.
- **Bowlers** concede runs off the bat plus bowler-error extras (wides and no-balls). Byes, leg-byes, and penalty runs are fielding/keeper extras that are strictly excluded from bowler runs conceded.
- **Dismissals** must distinguish bowler-credited wickets (`Caught`, `Bowled`, `LBW`, `Stump`, `Hit Wicket`) from non-bowler wickets (`RunOut`, `Retire Out`, `Obstructing the field`) and injury stoppages (`Retired Hurt`).

This audit rigorously maps every single dismissal type and extra type present in the 200,999 delivery dataset, updates the attribution code in `src/stage_4_0/attribution.py`, and validates all eight mandatory governance assertions.

---

## 2. Comprehensive Event Attribution Mapping

The complete, authoritative mapping has been exported to `data/processed/player_attribution_event_mapping.csv`.

| Event Category | Event Type | Frequency in Data | Batter Attribution | Bowler Attribution | Batter VA Inclusion | Bowler VA Inclusion | Accounting Rationale |
|---|---|---:|---|---|:---:|:---:|---|
| **Dismissal** | `Caught` | 7,557 | Batter Execution Dismissal | Bowler Wicket Credited | **Yes** | **Yes** | Standard execution dismissal off bat to fielder or keeper. |
| **Dismissal** | `Bowled` | 1,775 | Batter Execution Dismissal | Bowler Wicket Credited | **Yes** | **Yes** | Stumps broken by legal delivery. Clean bowler credit. |
| **Dismissal** | `LBW` | 709 | Batter Execution Dismissal | Bowler Wicket Credited | **Yes** | **Yes** | Batsman pinned in front; umpire dismissal. |
| **Dismissal** | `RunOut` | 600 | Non-Standard (Running Fault) | **Team Wicket (NOT Bowler)** | **No** | **No** | Run outs reflect running mix-up/fielding excellence, not bowler delivery quality. |
| **Dismissal** | `Stump` | 214 | Batter Execution Dismissal | Bowler Wicket Credited | **Yes** | **Yes** | Batsman deceived out of crease by bowler; wicketkeeper executes. |
| **Dismissal** | `Hit Wicket` | 17 | Batter Execution Dismissal | Bowler Wicket Credited | **Yes** | **Yes** | Batsman breaks stumps in preparation or follow-through. |
| **Dismissal** | `Retire Out` | 6 | Tactical Team Retirement | **Team Wicket (NOT Bowler)** | **No** | **No** | Voluntary exit for team batting strategy; not a delivery-level out. |
| **Dismissal** | `Obstructing the field` | 3 | Batsman Infraction / Penalty | **Team Wicket (NOT Bowler)** | **No** | **No** | Wilful batsman obstruction; team dismissal not bowler wicket. |
| **Dismissal** | `Retired Hurt` | 12 | Medical / Injury Stoppage | **No Wicket (NOT Bowler)** | **No** | **No** | Player leaves field due to injury; zero wickets charged to team/bowler. |
| **Extras** | `wide` | 7,714 | Excluded from Batter Balls | **Charged to Bowler (1 + extras)** | **No** | **Yes** | Bowler illegal delivery; charged strictly to bowler conceded. |
| **Extras** | `legbyes` | 2,748 | 0 Bat Runs Credited | **EXCLUDED from Bowler Conceded** | **No** | **No** | Deflection off pad; standard cricket law excludes from bowler conceded. |
| **Extras** | `Overstep` | 576 | Bat Runs Credited to Striker | **Charged to Bowler (Bat + 1)** | **Yes** | **Yes** | Foot-fault no-ball; bowler penalized, batter receives runs off bat. |
| **Extras** | `byes` | 529 | 0 Bat Runs Credited | **EXCLUDED from Bowler Conceded** | **No** | **No** | Wicketkeeper / fielding lapse; excluded from bowler runs conceded. |
| **Extras** | `other` | 264 | Bat Runs Credited to Striker | **Charged to Bowler (Bat + 1)** | **Yes** | **Yes** | Other no-balls (waist-high full toss, field restriction breach). |
| **Extras** | `Penalty` | 1 | 0 Bat Runs Credited | **EXCLUDED from Bowler Conceded** | **No** | **No** | 5 penalty runs (ball hit helmet behind keeper); team penalty. |
| **Standard** | `None` (Legal) | 189,167 | Bat Runs Credited to Striker | Bat Runs Charged to Bowler | **Yes** | **Yes** | Standard legal delivery; clean attribution to both actors. |

---

## 3. Mandatory Governance Assertions Audit

All eight executable assertions were verified programmatically by running `src/stage_4_0/attribution_audit.py`:

```
================================================================================
Attribution Verification Assertions (Full Dataset: 200,999 deliveries)
================================================================================
  [Assertion 1 PASS] Every dismissal type in dataset is formally classified.
  [Assertion 2 PASS] Every extra type in dataset is formally classified.
  [Assertion 3 PASS] No unexplained attribution categories exist.
  [Assertion 4 PASS] Batter metrics strictly exclude byes, leg-byes, and wides.
  [Assertion 5 PASS] Bowler conceded runs strictly exclude byes, leg-byes, and penalty runs.
  [Assertion 6 PASS] Run-outs are strictly isolated as team wickets, NOT bowler wickets.
  [Assertion 7 PASS] Retired hurt (12 events) is strictly isolated; zero wickets charged to team/bowler.
  [Assertion 8 PASS] Retired out is separately documented as tactical retirement (6 events).
================================================================================
```

---

## 4. Methodological Impact on Value Added (VA)

1. **Batter Value Added ($\text{RVA}$):**
   $$\text{RVA}(t) = \text{runs\_off\_bat}(t) - \hat{\mu}_{\text{runs}}(t^-)$$
   Byes (529 deliveries), leg-byes (2,748 deliveries), and penalties (1 delivery) no longer artificially inflate batter run value. Wides (7,714 deliveries) are not credited as batter balls faced.

2. **Bowler Value Added ($\text{RCS}$):**
   $$\text{RCS}(t) = \hat{\mu}_{\text{runs}}(t^-) - \text{bowler\_runs\_conceded}(t)$$
   where:
   $$\text{bowler\_runs\_conceded} = \begin{cases}
   \text{runs\_off\_bat} + \text{extras\_runs}, & \text{if extras\_type} \in \{\text{'wide'}, \text{'Overstep'}, \text{'other'}\} \\
   \text{runs\_off\_bat}, & \text{if extras\_type} \in \{\text{None}, \text{'byes'}, \text{'legbyes'}, \text{'Penalty'}\}
   \end{cases}$$
   Bowlers are no longer penalized for keeper byes or leg-byes.

3. **Wicket Attribution:**
   Bowler wicket rate strictly counts `is_bowler_wicket == 1` ($10,272$ wickets). Run-outs ($600$), retire out ($6$), and obstructing the field ($3$) are completely excluded from bowler credit.

*Document Approved by PinkOps Quantitative Governance Committee.*
