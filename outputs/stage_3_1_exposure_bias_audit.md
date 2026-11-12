# PinkOps — Stage 3.1: Participation & Exposure-Bias Audit
**Project**: Operation Pink Panther  
**Brand**: PinkOps  
**Output Data Reference**: [`data/processed/stage_3_1_player_exposure.csv`](file:///D:/PinkOps/data/processed/stage_3_1_player_exposure.csv)  
**Dataset Reference**: [`data/processed/match_state.parquet`](file:///D:/PinkOps/data/processed/match_state.parquet) (200,999 deliveries, 867 matches)  

---

## 1. Executive Summary & Audit Mandate

In player evaluation under pressure, **exposure bias** poses a dual hazard:
1. **The Small-Sample Outlier Trap**: A player with 12 deliveries who hits three boundaries in one chase can achieve an astronomical raw Value Added ($+1.8$ runs/ball), appearing superior to an established international star who has maintained $+0.35$ runs/ball over 300 pressure deliveries.
2. **The Truncation Injustice**: An arbitrary rule like "minimum 100 high-pressure balls" discards 85% of batters, completely erasing specialist lower-order death finishers (#6/#7) who face only 8–12 balls per match.

**PinkOps Protocol**: We neither truncate players arbitrarily nor evaluate small samples naively. Instead, we:
- Profile empirical exposure distributions across all 1,535 player-roles.
- Formalize a three-tier **Evidence Taxonomy**.
- Regulate small samples using **Empirical Bayes shrinkage** and **Lower Credible Bounds (LCB)**.
- Retain sample size and uncertainty width explicitly in every player evidence vector.

---

## 2. Empirical Exposure Profiling (888 Batters & 647 Bowlers)

### Batting Delivery Exposure Distribution
- **Total Unique Batters**: 888
- **Total Deliveries Faced Distribution**:
  - Min: 1 ball
  - P10: 5 balls
  - P25: 16 balls
  - **Median: 54 balls**
  - P75: 189 balls
  - P90: 716 balls
  - P95: 1,131 balls
  - Max: 2,920 balls
- **High-Pressure Deliveries (RRR $\ge 10$, Death, or Crisis RDI $\ge 5.0$)**:
  - Median: **14 balls**
  - Only **250 batters (28.2%)** have faced $\ge 40$ high-pressure deliveries.
  - Over **462 batters (52.0%)** have faced fewer than 15 pressure deliveries.

### Bowling Delivery Exposure Distribution
- **Total Unique Bowlers**: 647
- **Total Deliveries Bowled Distribution**:
  - Min: 1 ball
  - P25: 36 balls
  - **Median: 108 balls**
  - P75: 351 balls
  - Max: 3,207 balls
- **High-Pressure Deliveries**:
  - Median: **28 balls**
  - **273 bowlers (42.2%)** have bowled $\ge 40$ high-pressure deliveries.
  - **215 bowlers (33.2%)** have bowled fewer than 15 pressure deliveries.

---

## 3. The PinkOps Evidence Taxonomy

Every player-role in the competition dataset is assigned to an objective **Evidence Depth Tier**:

| Evidence Tier | Defining Criteria | Batters Count | Bowlers Count | Total Players | Analytical Treatment |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Robust Evidence** | $\ge 150$ total balls **AND** $\ge 40$ pressure balls | **250** (28.2%) | **273** (42.2%) | **523** (34.1%) | Empirical data dominates posterior; tight confidence intervals; eligible for top reliability tiers |
| **Moderate Evidence** | $\ge 50$ total balls **AND** $\ge 15$ pressure balls | **176** (19.8%) | **159** (24.6%) | **335** (21.8%) | Moderate Empirical Bayes shrinkage toward prior; wider confidence bands; high-potential watch candidates |
| **Low / Sparse Evidence**| $< 50$ total balls **OR** $< 15$ pressure balls | **462** (52.0%) | **215** (33.2%) | **677** (44.1%) | Heavy shrinkage toward prior; wide posterior uncertainty; flagged with `is_low_exposure = 1` |

---

## 4. Why Arbitrary Truncation Fails in T20 Cricket

Consider a franchise finisher batting at No. 6 or No. 7:
- Average entry point: Over 16.2.
- Average balls faced per match: 9.4 balls.
- If a franchise plays 14 matches a season, and the team chases in 7 matches with high RRR in 3 of them, the player faces only **~28 high-pressure balls in an entire year**!
- An arbitrary gate of "minimum 100 pressure balls" would require this finisher to play 4 full seasons without missing a game before becoming eligible for evaluation.
- Meanwhile, top-order openers face 35 balls every game and reach 100 balls in 3 matches.

**Solution**: By retaining all players and applying **Empirical Bayes shrinkage** ($K = 100$ pseudo-observations), a finisher with 30 exceptional pressure balls has their performance shrunk moderately ($\lambda = 30 / 130 \approx 23\%$), pulling extreme noise out of their numbers while preserving the undeniable evidence of their finishing impact.

---

## 5. Exposure Bias Mitigation Standards for Downstream Stages

1. **No player is ever evaluated on un-shrunk raw averages.**
2. **Every player output dossier must report both Posterior Mean and Posterior LCB (20th percentile).**
3. **The Evidence Tier flag (`Robust`, `Moderate`, `Low`) must accompany all player metrics.**
4. A player with 12 excellent pressure balls will never be placed on equal footing with a player with 150 excellent pressure balls, because their 95% confidence interval width ($2 \times 1.96 \times \text{SE}$) will be over $3.5\times$ wider, naturally penalizing them in conservative decision-making.

---
*Report compiled by PinkOps Data Engineering Team | Operation Pink Panther*
