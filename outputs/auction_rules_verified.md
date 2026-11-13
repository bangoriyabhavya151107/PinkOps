# PinkOps — Stage 5: Competition Problem Statement & Auction Rules Verification Audit
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Tagline:** Finding the Next Legend  
**Working Slogan:** Zero Choke. All Smoke.  
**Source Document:** [`data/raw/6af458274c1e8_data_pack/Data Pack/Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`](file:///D:/PinkOps/data/raw/6af458274c1e8_data_pack/Data%20Pack/Round%201%20Problem%20Statement%20_%20SupeRR%20Selector%20Season%202.docx.pdf)  
**Date:** November 2026  

---

## 1. Audit Objective & Governance Standard

In strict accordance with the **PinkOps Analysis Constitution (Rule 1 & Rule 13)** and **Stage 5 Governance Rule 2.2**:
> *"Never invent player statistics, missing observations, auction prices, player roles unsupported by data, squad rules, budget rules, competition scoring rules, player availability, or historical performance. If something cannot be established from the available data, mark it UNKNOWN or NOT OBSERVABLE."*

This document extracts and audits all verified rules from the official competition materials provided in [`data/raw/`](file:///D:/PinkOps/data/raw/) prior to formulating any player selection or auction strategy.

---

## 2. Extraction from Official Round 1 Problem Statement

The official problem statement PDF (`Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`) was programmatically inspected and extracted using `pypdf`. The document consists of two pages containing the following provisions:

### Page 1 Summary
- **Competition Title:** SupeRR Selector Season 2 — Round 1 Problem Statement: *"Identify the Most Reliable Players Under Pressure"*.
- **Core Challenge:** Build a data-driven system that measures how batters and bowlers perform in high-pressure match situations compared with their usual performance levels. Use the system to identify and rank the players who deliver most consistently when it matters.
- **Definition of Pressure:** Left entirely to the participant to define (*"What counts as pressure? That is for you to define... Required run rate, wickets in hand, balls remaining, stage of innings, contest closeness, or a combination of factors"*).
- **Supplied Data:** Historical IPL and T20 International (T20I) data from 2022 onwards, comprising delivery-level ball-by-ball records, competitions, teams, matches, playing elevens, and competition-team-player mappings.
- **Submission Components:**
  1. **Player Rankings:** Two ordered top-10 lists: the 10 best-performing batters under pressure and the 10 best-performing bowlers under pressure. Selected in rank order from 1 to 10 using dropdowns on Unstop.
  2. **Methodology Report:** A document upload explaining pressure definition, ratings construction, data analysis, and rationale for final rankings.

### Page 2 Summary
- **Dropdown Mechanics:** Rank 1 through Rank 10 for batters, and Rank 1 through Rank 10 for bowlers. Rank 1 is the highest-rated player. No duplicate players within the same top-10 list.
- **Report Requirements:** Must cover Pressure Definition, Performance Measurement, Fair Comparisons (sample sizes, eligibility, IPL vs T20I context), Evidence for Top 10, and Reliability & Limitations.
- **Explicit Instruction:** *"Rankings must be supported by analysis of the supplied data, not reputation alone."*
- **Optional Submission:** Short video or journey reflection (explicitly non-evaluative).

---

## 3. Explicit Verification Matrix: What Is vs. Is Not in Official Rules

| Parameter / Rule Domain | Status in Official Round 1 Materials | Official Rule Citation / Text | Analytical Treatment in PinkOps |
| :--- | :---: | :--- | :--- |
| **Top 10 Batters List** | **VERIFIED** | *"Two ordered top-10 lists: the 10 best-performing batters under pressure... Rank 1 through Rank 10."* | Output exactly 10 ordered batters in `outputs/final_10_batters.csv` & `.md`. |
| **Top 10 Bowlers List** | **VERIFIED** | *"Two ordered top-10 lists: the 10 best-performing bowlers under pressure... Rank 1 through Rank 10."* | Output exactly 10 ordered bowlers in `outputs/final_10_bowlers.csv` & `.md`. |
| **Methodology Report Upload** | **VERIFIED** | *"Upload a document that explains how you defined pressure, constructed your ratings, analysed the data, and arrived at your final rankings."* | Built comprehensive methodology suite across `outputs/`. |
| **No Reputation Bias** | **VERIFIED** | *"Rankings must be supported by analysis of the supplied data, not reputation alone."* | Strict adherence: zero reputation weight; data-driven metrics only. |
| **Data Scope (IPL + T20I, 2022+)** | **VERIFIED** | *"Historical IPL and T20 International (T20I) data from 2022 onwards..."* | 200,999 deliveries across 867 contested matches (IPL & T20I). |
| **Auction Total Purse / Budget** | **NOT SPECIFIED / UNVERIFIED** | *No mention in Round 1 Problem Statement PDF.* | **DO NOT FABRICATE.** Marked `NOT OBSERVABLE`. |
| **Individual Player Salary Caps / Bid Max** | **NOT SPECIFIED / UNVERIFIED** | *No mention in Round 1 Problem Statement PDF.* | **DO NOT FABRICATE.** Marked `NOT OBSERVABLE`. |
| **Squad Size Minimum / Maximum** | **NOT SPECIFIED / UNVERIFIED** | *No mention in Round 1 Problem Statement PDF.* | **DO NOT FABRICATE.** Marked `NOT OBSERVABLE`. |
| **Overseas Player Limits (Foreign Quota)**| **NOT SPECIFIED / UNVERIFIED** | *No mention in Round 1 Problem Statement PDF.* | **DO NOT FABRICATE.** Marked `NOT OBSERVABLE`. |
| **Player Retention / RTM Rules** | **NOT SPECIFIED / UNVERIFIED** | *No mention in Round 1 Problem Statement PDF.* | **DO NOT FABRICATE.** Marked `NOT OBSERVABLE`. |
| **Bidding Increment Mechanics** | **NOT SPECIFIED / UNVERIFIED** | *No mention in Round 1 Problem Statement PDF.* | **DO NOT FABRICATE.** Marked `NOT OBSERVABLE`. |

---

## 4. Methodological Implications for Stage 5 Auction Strategy

Because the Round 1 prompt specifies a **pure player identification and ranking mandate** without a defined numerical purse or mock bidding engine:

1. **Zero Price Fabrication:**  
   PinkOps will **never invent fictitious monetary valuations** (e.g. claiming a player is "worth ₹14.5 Crore" without an empirical salary model or competition auction engine).
2. **Strategic Tiered Acquisition Framework:**  
   In place of fabricated rupee values, PinkOps provides franchise leadership with a **qualitative, decision-theoretic auction board**:
   - **MUST TARGET:** High-conviction, Tier-1 candidates with robust sample size, top-quartile performance, positive LUB20, and universal multiverse support.
   - **TARGET:** Elite specialized performers with strong evidence in defined tactical roles (e.g. Death Specialists or Powerplay Anchors).
   - **VALUE TARGET:** High-efficiency performers whose statistical value-added is under-appreciated relative to popular reputation.
   - **BACKUP:** Validated role-equivalent alternatives to ensure squad resilience if primary targets face intense bidding.
   - **AVOID OVERPAY:** High-reputation players whose empirical downside risk (e.g. early dismissal rate > 20%) or elevated uncertainty does not warrant aggressive bidding.
3. **Contingent Decision Tree:**  
   An operational protocol governing bidding behavior based on role equivalence, robustness support, and downside thresholds rather than imaginary purse decrements.

---

*End of Auction Rules Verification Audit.*
