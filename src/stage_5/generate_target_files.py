"""
PinkOps — Stage 5: Target Files Generator for All 20 Final Players
Module: src/stage_5/generate_target_files.py

Purpose:
- Generates 20 individual target dossier files in outputs/target_files/:
  * 10 Batters (ranks 1 to 10)
  * 10 Bowlers (ranks 1 to 10)
- Each dossier includes:
  1. PLAYER
  2. ROLE (Primary & Secondary)
  3. WHY PINKOPS SHOULD TARGET THEM
  4. PERFORMANCE EVIDENCE (Spec B Contextual Model)
  5. PRESSURE EVIDENCE (PI_80 & CEM Matched Contrast)
  6. RELIABILITY (Empirical Bayes Shrinkage & Downside Floor)
  7. UNCERTAINTY (SE_EB & Normal-Normal Confidence Bounds)
  8. SAMPLE SIZE (Deliveries, Matches, Competitions)
  9. ROBUSTNESS (Multiverse Specification Support & Sign Stability)
  10. DOWNSIDE (Early Dismissal / Blowout Rate)
  11. BEST TACTICAL USE
  12. WORST TACTICAL USE
  13. FAILURE CONDITIONS
  14. COMPARABLE ALTERNATIVES (Side-by-side metric comparison)
  15. KEY STATISTICS (Tabular summary)
  16. DATA LIMITATIONS
"""

import json
import pandas as pd
from pathlib import Path

def generate_all_target_files(project_root: Path):
    outputs_dir = project_root / "outputs"
    target_dir = outputs_dir / "target_files"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    bat_csv = outputs_dir / "final_10_batters.csv"
    bowl_csv = outputs_dir / "final_10_bowlers.csv"
    evidence_parquet = project_root / "data" / "processed" / "stage_5_player_evidence.parquet"
    
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    df_ev = pd.read_parquet(evidence_parquet)
    
    print("Generating 10 Batter Target Dossiers...")
    
    batter_metadata = [
        {
            "rank": 1, "id": 37052, "slug": "player_1_naman_dhir", "name": "Naman Dhir",
            "primary": "Finisher / Death Specialist", "secondary": "Middle-Overs Accelerator",
            "why": "Naman Dhir establishes the highest conservative lower uncertainty bound (LUB20 = +0.1918) across the entire 1,535-player competition universe. He combines blistering death-overs boundary execution (71.4% boundary run share) with remarkably low match variance (MAD = 0.4059) and controlled early dismissal risk (17.4%).",
            "best_use": "Entry at overs 15–18 during steep chases requiring 10.5+ rpo. Immediate license to attack pace and spin into the leg-side arc.",
            "worst_use": "Powerplay pinch-hitting against swinging new-ball pace on green-tinged surfaces.",
            "failure_cond": "Sustained wide-line outside-off yorkers with deep point and deep cover boundary protection; bowler variations taking pace off into a sticky surface.",
            "alt_1": {"name": "Tim David", "role": "Finisher / Death Specialist", "perf": "+0.1665", "lub": "+0.1326", "press": "+0.1893", "se": "0.0403", "n": "1,293", "down": "19.4%", "rob": "8/8"},
            "alt_2": {"name": "Jitesh Sharma", "role": "Finisher / Death Specialist", "perf": "+0.1538", "lub": "+0.1103", "press": "+0.1889", "se": "0.0517", "n": "926", "down": "17.8%", "rob": "8/8"},
            "limitations": "Dataset captures 603 total legal deliveries since 2022; smaller sample relative to decade-long international veterans, though thoroughly cleared by Bayesian shrinkage."
        },
        {
            "rank": 2, "id": 1699, "slug": "player_2_suryakumar_yadav", "name": "Suryakumar Yadav",
            "primary": "Middle-Overs Accelerator", "secondary": "360-Degree Pressure Enforcer",
            "why": "Suryakumar Yadav is the premier T20 middle-overs match-winner in world cricket. Backed by 2,848 deliveries and 908 high-pressure balls faced, his epistemic uncertainty is minuscule (SE = 0.0363), giving him an impregnable LUB20 of +0.0893 with universal 8/8 multiverse support and a modest early dismissal rate of 16.6%.",
            "best_use": "Entry in overs 7–11 following a solid powerplay base. Complete tactical freedom to manipulate field sets via sweeps, ramps, and lofted drives over extra cover.",
            "worst_use": "Sending him in as an emergency opener against swinging pace bowling in overcast conditions.",
            "failure_cond": "Disciplined extreme pace (148+ km/h) into the body targeting the ribs, backed by two deep square boundary fielders and deep fine leg.",
            "alt_1": {"name": "Fakhar Zaman", "role": "Middle-Overs Accelerator", "perf": "+0.1177", "lub": "+0.0655", "press": "+0.1576", "se": "0.0620", "n": "889", "down": "10.6%", "rob": "8/8"},
            "alt_2": {"name": "Rajat Patidar", "role": "Middle-Overs Accelerator", "perf": "+0.1148", "lub": "+0.0573", "press": "+0.1619", "se": "0.0683", "n": "970", "down": "12.5%", "rob": "8/8"},
            "limitations": "Extremely high market profile; will command peak acquisition interest in any open market environment."
        },
        {
            "rank": 3, "id": 6396, "slug": "player_3_tim_david", "name": "Tim David",
            "primary": "Finisher / Death Specialist", "secondary": "Pure Death Power Hitter",
            "why": "Tim David provides premier physical boundary clearing at the death. Facing 735 high-pressure deliveries (56.8% pressure exposure), he delivers an outstanding Empirical Bayes estimate (+0.1665) and the second-highest LUB20 among robust batters (+0.1326), backed by an early dismissal rate under 20% (19.4%).",
            "best_use": "Designated finisher batting at No. 6 or No. 7 from over 14 onwards. Target straight and mid-wicket boundaries against hard-length death bowling.",
            "worst_use": "Promoting him into the top order to anchor a rebuilding phase after 3 early powerplay wickets.",
            "failure_cond": "Tacky, gripped turning pitches where spinners fire flat into the front pad and deny straight arm extension.",
            "alt_1": {"name": "Naman Dhir", "role": "Finisher / Death Specialist", "perf": "+0.2443", "lub": "+0.1918", "press": "+0.3270", "se": "0.0624", "n": "603", "down": "17.4%", "rob": "8/8"},
            "alt_2": {"name": "Nicholas Pooran", "role": "Finisher / Death Specialist", "perf": "+0.0633", "lub": "+0.0305", "press": "+0.0838", "se": "0.0389", "n": "2,091", "down": "14.8%", "rob": "8/8"},
            "limitations": "Moderately elevated match MAD (0.5246) reflecting boundary-dominated outcome variance."
        },
        {
            "rank": 4, "id": 6819, "slug": "player_4_yashasvi_jaiswal", "name": "Yashasvi Jaiswal",
            "primary": "Top-Order Anchor / Powerplay Batter", "secondary": "Powerplay Enforcer",
            "why": "Yashasvi Jaiswal combines elite powerplay aggression with elite stability. Across 1,936 legal deliveries, he maintains the lowest match dispersion among aggressive openers (MAD = 0.2880) and an exceptionally low early dismissal rate (14.6%), translating to a solid LUB20 of +0.0795 and unanimous multiverse support.",
            "best_use": "First-choice opening batter. Attacking new-ball seamers over the infield during the first 6 overs to establish an early run-rate advantage.",
            "worst_use": "Holding him back to bat in the middle order after over 10.",
            "failure_cond": "High-quality left-arm inswinging pace pitching on good length and darting back through the gate in early overs.",
            "alt_1": {"name": "Brian Bennett", "role": "Top-Order Anchor / Powerplay", "perf": "+0.1429", "lub": "+0.0674", "press": "+0.2632", "se": "0.0897", "n": "815", "down": "22.7%", "rob": "8/8"},
            "alt_2": {"name": "Phil Salt", "role": "Top-Order Anchor / Powerplay", "perf": "+0.1537", "lub": "+0.0753", "press": "+0.2842", "se": "0.0931", "n": "1,700", "down": "25.0%", "rob": "8/8"},
            "limitations": "Because powerplay overs rarely meet the continuous PI >= 0.5898 threshold in first innings, raw pressure balls faced (77) is smaller than middle/death batters."
        },
        {
            "rank": 5, "id": 3916, "slug": "player_5_jitesh_sharma", "name": "Jitesh Sharma",
            "primary": "Finisher / Death Specialist", "secondary": "Wicketkeeper-Finisher",
            "why": "Jitesh Sharma is one of the most efficient domestic Indian death-overs assets in existence. Across 926 balls (438 pressure deliveries), he generates +0.1538 value-added per ball, an outstanding LUB20 of +0.1103, and an early dismissal rate of only 17.8%, with low match-to-match volatility (MAD = 0.3455).",
            "best_use": "Wicketkeeper-finisher at No. 5 or No. 6. Scoring immediately from ball one through innovative 360-degree boundary placement behind the wicket.",
            "worst_use": "Asking him to anchor a 120-run target in first gear with multiple defensive singles.",
            "failure_cond": "Consistently hostile short-pitched bouncers aimed directly at the helmet grille from high-release fast bowlers.",
            "alt_1": {"name": "Dinesh Karthik", "role": "Finisher / Death Specialist", "perf": "+0.1026", "lub": "+0.0627", "press": "+0.1241", "se": "0.0474", "n": "683", "down": "14.8%", "rob": "8/8"},
            "alt_2": {"name": "Naman Dhir", "role": "Finisher / Death Specialist", "perf": "+0.2443", "lub": "+0.1918", "press": "+0.3270", "se": "0.0624", "n": "603", "down": "17.4%", "rob": "8/8"},
            "limitations": "Requires strict situational deployment; does not possess traditional defensive anchor technique for multi-day formats."
        },
        {
            "rank": 6, "id": 2921, "slug": "player_6_fakhar_zaman", "name": "Fakhar Zaman",
            "primary": "Middle-Overs Accelerator", "secondary": "Middle-Overs Anchor / Chase Master",
            "why": "Fakhar Zaman boasts the lowest early dismissal rate (10.64%) among all high-performing middle-order batters in the competition. He delivers +0.1177 value-added per ball, an LUB20 of +0.0655 across 889 deliveries (295 pressure balls), and outstanding chase resilience.",
            "best_use": "No. 3 or No. 4 in chase scenarios requiring calculated acceleration against middle-overs spin.",
            "worst_use": "Opening against express swinging new ball on responsive seam-friendly green surfaces.",
            "failure_cond": "Accurate off-spin darted into the blockhole combined with an off-side boundary ring preventing lofted cover drives.",
            "alt_1": {"name": "Rajat Patidar", "role": "Middle-Overs Accelerator", "perf": "+0.1148", "lub": "+0.0573", "press": "+0.1619", "se": "0.0683", "n": "970", "down": "12.5%", "rob": "8/8"},
            "alt_2": {"name": "Suryakumar Yadav", "role": "Middle-Overs Accelerator", "perf": "+0.1199", "lub": "+0.0893", "press": "+0.1320", "se": "0.0363", "n": "2,848", "down": "16.6%", "rob": "8/8"},
            "limitations": "Slightly higher dot-ball percentage early in innings before accelerating into boundary flow."
        },
        {
            "rank": 7, "id": 5039, "slug": "player_7_rajat_patidar", "name": "Rajat Patidar",
            "primary": "Middle-Overs Accelerator", "secondary": "Spin Dominator",
            "why": "Rajat Patidar is an elite spin enforcer. Across 970 deliveries (237 pressure balls), he achieves +0.1148 value added per ball, an LUB20 of +0.0573, an early dismissal rate of only 12.50%, and unanimous multiverse support, dismantling middle-overs spin bowling with immense authority.",
            "best_use": "Batting at No. 4 specifically deployed when opposition introduces wrist-spin or finger-spin tandems in overs 7–14.",
            "worst_use": "Opening against high-pace swinging seamers in powerplay conditions.",
            "failure_cond": "Sustained bodyline short balls delivered at 145+ km/h by tall pacers with a deep backward square leg.",
            "alt_1": {"name": "Fakhar Zaman", "role": "Middle-Overs Accelerator", "perf": "+0.1177", "lub": "+0.0655", "press": "+0.1576", "se": "0.0620", "n": "889", "down": "10.6%", "rob": "8/8"},
            "alt_2": {"name": "Glenn Maxwell", "role": "Middle-Overs Accelerator", "perf": "+0.1057", "lub": "+0.0581", "press": "+0.1512", "se": "0.0565", "n": "1,004", "down": "30.7%", "rob": "8/8"},
            "limitations": "Specialist spin-dominant profile; relative output dips when confronted with elite fast-bowling enforcers."
        },
        {
            "rank": 8, "id": 24017, "slug": "player_8_brian_bennett", "name": "Brian Bennett",
            "primary": "Top-Order Anchor / Powerplay Batter", "secondary": "Aggressive Stabilizer",
            "why": "Brian Bennett represents an exceptional emerging international top-order talent. Across 815 deliveries (119 pressure balls), he achieves an EB estimate of +0.1429, an LUB20 of +0.0674, a low match MAD of 0.3091, and unanimous multiverse support.",
            "best_use": "Aggressive top-order batter in overs 1–10, capitalizing on field restrictions and setting an elevated scoring pace.",
            "worst_use": "Late-death entry at No. 7 with 8 balls remaining in the innings.",
            "failure_cond": "Stifling finger spin with deep mid-wicket boundary catchers cutting off pull shots.",
            "alt_1": {"name": "Yashasvi Jaiswal", "role": "Top-Order Anchor / Powerplay", "perf": "+0.1666", "lub": "+0.0795", "press": "+0.3831", "se": "0.1034", "n": "1,936", "down": "14.6%", "rob": "8/8"},
            "alt_2": {"name": "Shai Hope", "role": "Top-Order Anchor / Powerplay", "perf": "+0.1037", "lub": "+0.0434", "press": "+0.1528", "se": "0.0716", "n": "1,128", "down": "19.0%", "rob": "8/8"},
            "limitations": "Slightly higher early dismissal rate (22.7%) when attacking elite international new-ball pace."
        },
        {
            "rank": 9, "id": 4369, "slug": "player_9_shai_hope", "name": "Shai Hope",
            "primary": "Top-Order Anchor / Powerplay Batter", "secondary": "Middle-Overs Anchor / WK",
            "why": "Shai Hope is the consummate collapse-prevention anchor. Facing 211 high-pressure chase deliveries across 1,128 balls, he delivers an EB estimate of +0.1037, an LUB20 of +0.0434, and controlled early dismissal risk (19.0%), providing vital lineup security.",
            "best_use": "Top-order anchor at No. 3 in chases on tricky, two-paced, or spin-friendly tracks requiring calculated tempo.",
            "worst_use": "Death-overs designated hitter requiring 14 runs per over from ball one.",
            "failure_cond": "Extreme high-scoring shootouts where par score exceeds 220 and anchoring carries high opportunity cost.",
            "alt_1": {"name": "Brian Bennett", "role": "Top-Order Anchor / Powerplay", "perf": "+0.1429", "lub": "+0.0674", "press": "+0.2632", "se": "0.0897", "n": "815", "down": "22.7%", "rob": "8/8"},
            "alt_2": {"name": "Faf du Plessis", "role": "Top-Order Anchor / Powerplay", "perf": "+0.0817", "lub": "+0.0110", "press": "+0.1082", "se": "0.0839", "n": "1,306", "down": "5.6%", "rob": "7/8"},
            "limitations": "Lower absolute boundary ceiling compared to hyper-aggressive opening basher archetypes."
        },
        {
            "rank": 10, "id": 3125, "slug": "player_10_nicholas_pooran", "name": "Nicholas Pooran",
            "primary": "Finisher / Death Specialist", "secondary": "Left-Handed Middle Accelerator",
            "why": "Nicholas Pooran brings massive historical volume (2,091 balls faced, 789 pressure deliveries) with a low early dismissal rate (14.8%) and proven left-handed boundary clearing. He guarantees positive LUB20 (+0.0305) and unanimous 8/8 multiverse support.",
            "best_use": "Floating left-handed enforcer entering between overs 11 and 16 to dismantle right-arm off-spin and medium pace.",
            "worst_use": "Opening the batting against specialized swinging left-arm pace.",
            "failure_cond": "Disciplined wide-line bowling outside off-stump with deep backward point and third man in place.",
            "alt_1": {"name": "Heinrich Klaasen", "role": "Finisher / Death Specialist", "perf": "+0.0383", "lub": "+0.0023", "press": "+0.0492", "se": "0.0427", "n": "1,480", "down": "11.1%", "rob": "6/8"},
            "alt_2": {"name": "Tim David", "role": "Finisher / Death Specialist", "perf": "+0.1665", "lub": "+0.1326", "press": "+0.1893", "se": "0.0403", "n": "1,293", "down": "19.4%", "rob": "8/8"},
            "limitations": "Moderately elevated match MAD (0.4837); requires tactical matchup protection against high-pace off-stump lines."
        }
    ]
    
    for b in batter_metadata:
        fpath = target_dir / f"{b['slug']}.md"
        row = df_ev[(df_ev['player_id'] == b['id']) & (df_ev['role'] == 'batter')].iloc[0]
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(f"# PinkOps Target File: {b['name']} (Batter Rank {b['rank']})\n")
            f.write("**Project:** Operation Pink Panther / PinkOps  \n")
            f.write("**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  \n")
            f.write(f"**Target ID:** `PINKOPS-TARGET-BAT-{b['rank']:02d}`  \n")
            f.write(f"**Player ID:** `{b['id']}`  \n")
            f.write(f"**Date:** November 2026  \n\n")
            f.write("---\n\n")
            f.write("## 1. PLAYER & ROLE PROFILE\n\n")
            f.write(f"- **Player Name:** {b['name']}\n")
            f.write(f"- **Primary Tactical Role:** {b['primary']}\n")
            f.write(f"- **Secondary Role:** {b['secondary']}\n")
            f.write(f"- **Teams in Dataset:** {row['teams']}\n")
            f.write(f"- **Competitions:** {row['competitions']} ({row['seasons']})\n")
            f.write(f"- **Evidence Tier:** {row['evidence_tier']} ({row['exposure_tier']})\n")
            f.write(f"- **Reliability Profile:** {row['reliability_profile']}\n\n")
            f.write("---\n\n")
            f.write("## 2. WHY PINKOPS SHOULD TARGET THEM\n\n")
            f.write(f"{b['why']}\n\n")
            f.write("---\n\n")
            f.write("## 3. MULTIDIMENSIONAL EVIDENCE AUDIT\n\n")
            f.write("### A. Performance Evidence (Spec B Contextual Model)\n")
            f.write(f"- **Actual Runs Scored:** {int(row['actual_runs']):,} runs across {int(row['n_deliveries_total']):,} deliveries\n")
            f.write(f"- **Contextual Expected Runs:** {row['expected_runs']:.1f} runs (Baseline: {row['mean_expected_runs']:.3f} runs/ball)\n")
            f.write(f"- **Total Value-Added:** **+{row['value_added_total']:.2f} runs** relative to expectation\n")
            f.write(f"- **Boundary Value:** {row['boundary_run_pct']*100:.1f}% of runs scored in boundaries\n")
            f.write(f"- **Strike Rotation:** {row['strike_rotation_pct']*100:.1f}% single/two rotation rate\n\n")
            f.write("### B. Pressure Performance & Clutch Contrast\n")
            f.write(f"- **Pressure Exposure (PI >= 0.5898):** {int(row['n_deliveries_pressure']):,} deliveries ({row['pressure_ratio']*100:.1f}% of total)\n")
            f.write(f"- **Pressure Value-Added (RVA):** **+{row['rva_per_ball_pressure']:.4f} runs/ball** under high leverage\n")
            f.write(f"- **Matched Clutch Contrast (CEM Delta):** {row['clutch_delta_rva']:+.4f} runs/ball elevation vs matched control\n")
            f.write(f"- **Strike Rate Under Pressure:** {row['strike_rate_pressure']:.1f} (Boundary %: {row['boundary_pct_pressure']*100:.1f}%)\n\n")
            f.write("### C. Reliability & Lower Uncertainty Bounds\n")
            f.write(f"- **Empirical Bayes Estimate (K=100):** **+{row['eb_shrunk_estimate']:.4f}**\n")
            f.write(f"- **Standard Error (SE_EB):** {row['se_eb']:.4f} ({row['uncertainty_tier']})\n")
            f.write(f"- **LUB20 (Downside Decision Floor):** **+{row['lub_20']:.4f}**\n")
            f.write(f"- **Quantile Multiverse Bounds:** LUB10: {row['lub_10']:+.4f} | LUB20: {row['lub_20']:+.4f} | LUB25: {row['lub_25']:+.4f} | LUB30: {row['lub_30']:+.4f}\n")
            f.write(f"- **Match-Level Dispersion:** MAD = {row['match_va_mad']:.4f} | IQR = {row['match_va_iqr']:.4f}\n\n")
            f.write("### D. Downside Risk Assessment\n")
            f.write(f"- **Early Dismissal Rate (<= 5 balls):** **{row['early_dismissal_rate']*100:.1f}%** (Governance Ceiling: 20.0%)\n")
            f.write(f"- **Pressure Collapse Rate:** {row['pressure_collapse_rate']*100:.1f}%\n")
            f.write(f"- **Negative Match Percentage:** {row['negative_match_pct']*100:.1f}%\n\n")
            f.write("### E. Multiverse Robustness Verification\n")
            f.write(f"- **Specifications Supported:** **{row['multiverse_specs_supported']}/8** ({row['multiverse_support_pct']:.1f}%)\n")
            f.write(f"- **Robustness Tier:** {row['robustness_tier']}\n")
            f.write(f"- **Spec A vs Spec B Stability:** Spec B LUB20 = +{row['spec_b_lub20']:.4f} vs Spec A LUB20 = +{row['spec_a_lub20']:.4f}\n\n")
            f.write("---\n\n")
            f.write("## 4. TACTICAL DEPLOYMENT BLUEPRINT\n\n")
            f.write(f"- **Best Tactical Use:** {b['best_use']}\n")
            f.write(f"- **Worst Tactical Use:** {b['worst_use']}\n")
            f.write(f"- **Primary Failure Conditions:** {b['failure_cond']}\n\n")
            f.write("---\n\n")
            f.write("## 5. COMPARABLE PLAYER ANALYSIS\n\n")
            f.write("| Candidate | Role | Contextual Perf | LUB20 | Pressure RVA | Uncertainty (SE) | Sample Size | Downside (EDR) | Robustness Support |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
            f.write(f"| **{b['name']} (Selected)** | {b['primary']} | +{row['eb_shrunk_estimate']:.4f} | **+{row['lub_20']:.4f}** | +{row['rva_per_ball_pressure']:.4f} | {row['se_eb']:.4f} | {int(row['n_deliveries_total']):,} | {row['early_dismissal_rate']*100:.1f}% | {row['multiverse_specs_supported']}/8 |\n")
            f.write(f"| {b['alt_1']['name']} (Alt 1) | {b['alt_1']['role']} | {b['alt_1']['perf']} | {b['alt_1']['lub']} | {b['alt_1']['press']} | {b['alt_1']['se']} | {b['alt_1']['n']} | {b['alt_1']['down']} | {b['alt_1']['rob']} |\n")
            f.write(f"| {b['alt_2']['name']} (Alt 2) | {b['alt_2']['role']} | {b['alt_2']['perf']} | {b['alt_2']['lub']} | {b['alt_2']['press']} | {b['alt_2']['se']} | {b['alt_2']['n']} | {b['alt_2']['down']} | {b['alt_2']['rob']} |\n\n")
            f.write("---\n\n")
            f.write("## 6. DATA LIMITATIONS\n\n")
            f.write(f"{b['limitations']}\n\n")
            f.write("---\n\n")
            f.write(f"*End of Target File for {b['name']}.*\n")
            
    print("Generating 10 Bowler Target Dossiers...")
    
    bowler_metadata = [
        {
            "rank": 1, "id": 2933, "slug": "player_11_jasprit_bumrah", "name": "Jasprit Bumrah",
            "primary": "Death Specialist (Pace)", "secondary": "All-Phase Bowling Enforcer",
            "why": "Jasprit Bumrah is the undisputed global benchmark for pressure execution in T20 bowling. Delivering an extraordinary EB run prevention rate (+0.3196 runs/ball) across 1,780 deliveries (697 pressure balls), he establishes an LUB20 of +0.2848, a microscopic blowout rate of only 9.26%, and universal multiverse support.",
            "best_use": "Bowling overs 17 and 19 in tight defenses/chases, and the pivotal over 13 to break momentum. Pinpoint yorkers and disguise slower balls.",
            "worst_use": "Exhausting his complete 4-over allocation inside the first 10 overs.",
            "failure_cond": "Extreme dew creating a greasy ball that impairs seam grip, yorker landing margin, and reverse swing.",
            "alt_1": {"name": "Matheesha Pathirana", "role": "Death Specialist (Pace)", "perf": "+0.1797", "lub": "+0.1449", "press": "+0.2198", "se": "0.0413", "n": "1,279", "down": "19.2%", "rob": "8/8"},
            "alt_2": {"name": "Jamie Overton", "role": "Death Specialist (Pace)", "perf": "+0.1941", "lub": "+0.1398", "press": "+0.2541", "se": "0.0645", "n": "525", "down": "17.2%", "rob": "8/8"},
            "limitations": "Opposition batters actively decline risk against him, resulting in containment rather than inflated raw wicket tallies."
        },
        {
            "rank": 2, "id": 781, "slug": "player_12_sunil_narine", "name": "Sunil Narine",
            "primary": "Middle Enforcer (Spin)", "secondary": "Spin Squeeze & Strike Bowler",
            "why": "Sunil Narine delivers the single highest run prevention rate (+0.3228 runs/ball) in competitive T20 cricket. Across 1,553 deliveries (579 pressure balls), he maintains an LUB20 of +0.2848, an extraordinarily low match MAD (0.2257), and a tiny blowout rate of only 8.00%.",
            "best_use": "Overs 7–15 to freeze opposition run scoring and force desperate attacking strokes into protected boundary riders.",
            "worst_use": "Bowling the 20th over against tall power hitters on ultra-short straight boundaries.",
            "failure_cond": "Small ground dimensions with heavily skewed boundaries where mis-hits travel 65 meters for six.",
            "alt_1": {"name": "Abrar Ahmed", "role": "Middle Enforcer (Spin)", "perf": "+0.2033", "lub": "+0.1556", "press": "+0.2581", "se": "0.0567", "n": "776", "down": "5.4%", "rob": "8/8"},
            "alt_2": {"name": "Mitchell Santner", "role": "Middle Enforcer (Spin)", "perf": "+0.1215", "lub": "+0.0882", "press": "+0.1396", "se": "0.0396", "n": "1,793", "down": "12.8%", "rob": "8/8"},
            "limitations": "Bowling action subjected to periodic intense scrutiny; tactical deployment relies on subtle variation rather than sharp drift."
        },
        {
            "rank": 3, "id": 5979, "slug": "player_13_abrar_ahmed", "name": "Abrar Ahmed",
            "primary": "Middle Enforcer (Spin)", "secondary": "Mystery Leg-Spin Attacker",
            "why": "Abrar Ahmed records the lowest blowout rate (5.41%) among all high-volume spin bowlers. Across 776 legal deliveries (359 pressure balls), he secures +0.2033 run prevention per ball, an LUB20 of +0.1556, and 46 wickets, proving elite middle-overs containment.",
            "best_use": "Attacking middle-overs spin enforcer in overs 8–14. Deploying googlies and carrom balls against middle-order right-handers.",
            "worst_use": "Bowling with a wet ball in heavy dew conditions against set batters.",
            "failure_cond": "Batters with elite sweep and reverse-sweep technique disrupting his length before release.",
            "alt_1": {"name": "Sai Kishore", "role": "Middle Enforcer (Spin)", "perf": "+0.1492", "lub": "+0.0865", "press": "+0.1983", "se": "0.0744", "n": "501", "down": "13.6%", "rob": "8/8"},
            "alt_2": {"name": "Sunil Narine", "role": "Middle Enforcer (Spin)", "perf": "+0.3228", "lub": "+0.2848", "press": "+0.4120", "se": "0.0451", "n": "1,553", "down": "8.0%", "rob": "8/8"},
            "limitations": "Slightly fewer total competitive T20 overs compared to veterans with 10+ franchise seasons."
        },
        {
            "rank": 4, "id": 8661, "slug": "player_14_matheesha_pathirana", "name": "Matheesha Pathirana",
            "primary": "Death Specialist (Pace)", "secondary": "Slingy Yorker Attacker",
            "why": "Matheesha Pathirana is a generational death-overs strike weapon. His sling-arm trajectory produces 82 wickets across 1,279 deliveries (strike rate 15.6), an EB run prevention rate of +0.1797, and an elite LUB20 of +0.1449 across 698 pressure balls.",
            "best_use": "Overs 16, 18, and 20. Firing unplayable dipping yorkers and sharp bouncers at high pace.",
            "worst_use": "Powerplay bowling with the new ball where radar and seam control can wander.",
            "failure_cond": "Excessive wide deliveries resulting from wide-line execution in breezy or dewy conditions.",
            "alt_1": {"name": "Jasprit Bumrah", "role": "Death Specialist (Pace)", "perf": "+0.3196", "lub": "+0.2848", "press": "+0.4082", "se": "0.0413", "n": "1,780", "down": "9.3%", "rob": "8/8"},
            "alt_2": {"name": "Josh Hazlewood", "role": "Death Specialist (Pace)", "perf": "+0.1255", "lub": "+0.0893", "press": "+0.1478", "se": "0.0430", "n": "1,515", "down": "17.7%", "rob": "8/8"},
            "limitations": "Slightly elevated extras rate (wides); physical load management required for sling-arm mechanics."
        },
        {
            "rank": 5, "id": 2382, "slug": "player_15_jamie_overton", "name": "Jamie Overton",
            "primary": "Death Specialist (Pace)", "secondary": "Heavy-Ball Middle Enforcer",
            "why": "Jamie Overton combines high pace with imposing release height. Across 525 deliveries (269 pressure balls), he delivers +0.1941 run prevention per ball, an LUB20 of +0.1398, a blowout rate of only 17.2%, and 36 wickets.",
            "best_use": "Hard-length enforcer through the middle and late overs (overs 11–18). Forcing top-edge catches off aggressive pulls.",
            "worst_use": "Full-length pitching on flat batting tracks with zero lateral movement.",
            "failure_cond": "Slow surfaces with low bounce where batters sit deep and swat hard length over mid-wicket.",
            "alt_1": {"name": "Kyle Jamieson", "role": "Powerplay Strike Pace", "perf": "+0.1363", "lub": "+0.0753", "press": "+0.1812", "se": "0.0724", "n": "668", "down": "12.9%", "rob": "8/8"},
            "alt_2": {"name": "Matheesha Pathirana", "role": "Death Specialist Pace", "perf": "+0.1797", "lub": "+0.1449", "press": "+0.2198", "se": "0.0413", "n": "1,279", "down": "19.2%", "rob": "8/8"},
            "limitations": "Slightly higher match MAD (0.4396) when batters successfully counter-attack his hard length."
        },
        {
            "rank": 6, "id": 2417, "slug": "player_16_akeal_hosein", "name": "Akeal Hosein",
            "primary": "Powerplay Specialist (Spin)", "secondary": "New-Ball Finger Spinner",
            "why": "Akeal Hosein delivers unprecedented powerplay containment. Across 1,734 legal deliveries (455 pressure balls), he achieves a 0.00% blowout rate (zero blowouts), the lowest match dispersion in cricket (MAD = 0.2122), an LUB20 of +0.0904, and 79 wickets.",
            "best_use": "Bowling overs 1, 3, and 5 in the powerplay. Under-cutting seamers with sliding arm-balls and pinpoint accuracy.",
            "worst_use": "Bowling overs 19 and 20 against designated death hitters.",
            "failure_cond": "Captain mismanaging his overs and leaving him to bowl at the death.",
            "alt_1": {"name": "Mitchell Santner", "role": "Middle Enforcer (Spin)", "perf": "+0.1215", "lub": "+0.0882", "press": "+0.1396", "se": "0.0396", "n": "1,793", "down": "12.8%", "rob": "8/8"},
            "alt_2": {"name": "Sai Kishore", "role": "Middle Enforcer (Spin)", "perf": "+0.1492", "lub": "+0.0865", "press": "+0.1983", "se": "0.0744", "n": "501", "down": "13.6%", "rob": "8/8"},
            "limitations": "Strict phase specialist; primary effectiveness is heavily concentrated in overs 1–10."
        },
        {
            "rank": 7, "id": 830, "slug": "player_17_josh_hazlewood", "name": "Josh Hazlewood",
            "primary": "Death Specialist (Pace)", "secondary": "Powerplay Line-and-Length Pacer",
            "why": "Josh Hazlewood is a master of relentless accuracy. Across 1,515 deliveries (641 pressure balls), he captures 98 wickets, generates +0.1255 run prevention per ball, and secures an LUB20 of +0.0893 with a controlled 17.7% blowout rate.",
            "best_use": "2 overs in the powerplay (overs 2 & 4) and 2 overs at the death (overs 17 & 19). Unyielding Test-match fourth-stump line.",
            "worst_use": "Middle overs on lifeless wickets when batters are looking to nudge singles without taking boundary risks.",
            "failure_cond": "360-degree batters ramping and scooping off-stump length deliveries over the keeper's head.",
            "alt_1": {"name": "Jasprit Bumrah", "role": "Death Specialist (Pace)", "perf": "+0.3196", "lub": "+0.2848", "press": "+0.4082", "se": "0.0413", "n": "1,780", "down": "9.3%", "rob": "8/8"},
            "alt_2": {"name": "Kyle Jamieson", "role": "Powerplay Strike Pace", "perf": "+0.1363", "lub": "+0.0753", "press": "+0.1812", "se": "0.0724", "n": "668", "down": "12.9%", "rob": "8/8"},
            "limitations": "Relies heavily on traditional seam and length discipline; fewer slower-ball knuckle variations."
        },
        {
            "rank": 8, "id": 4101, "slug": "player_18_mitchell_santner", "name": "Mitchell Santner",
            "primary": "Middle Enforcer (Spin)", "secondary": "All-Phase Finger Spinner",
            "why": "Mitchell Santner provides elite tournament-tested middle-overs control. Across 1,793 deliveries (767 pressure balls), he bags 87 wickets, delivers an LUB20 of +0.0882, and restricts blowouts to only 12.8%, with minimal epistemic uncertainty (SE = 0.0396).",
            "best_use": "Controlling the middle overs (overs 7–14). Altering release speed between 82 km/h and 98 km/h to deny batters boundary momentum.",
            "worst_use": "Bowling full deliveries into left-handed power hitters with short straight boundaries.",
            "failure_cond": "Opponents using advanced footwork to convert good length deliveries into half-volleys.",
            "alt_1": {"name": "Akeal Hosein", "role": "Powerplay Specialist Spin", "perf": "+0.1331", "lub": "+0.0904", "press": "+0.1584", "se": "0.0507", "n": "1,734", "down": "0.0%", "rob": "8/8"},
            "alt_2": {"name": "Sai Kishore", "role": "Middle Enforcer Spin", "perf": "+0.1492", "lub": "+0.0865", "press": "+0.1983", "se": "0.0744", "n": "501", "down": "13.6%", "rob": "8/8"},
            "limitations": "Defensive containment orientation produces fewer multi-wicket burst hauls."
        },
        {
            "rank": 9, "id": 5577, "slug": "player_19_sai_kishore", "name": "Sai Kishore",
            "primary": "Middle Enforcer (Spin)", "secondary": "Tall Left-Arm Spin Attacker",
            "why": "Sai Kishore is an elite domestic Indian spin weapon. Utilizing his high release point to extract sharp bounce, he captures 34 wickets across 501 deliveries (193 pressure balls), delivering an LUB20 of +0.0865 and a low 13.6% blowout rate.",
            "best_use": "Overs 7–13 against right-handed middle-order batters looking to hit through the line.",
            "worst_use": "Death-overs bowling in dewy conditions where seam grip is compromised.",
            "failure_cond": "Short boundary grounds with aggressive left-handed batters targeting the cow corner boundary.",
            "alt_1": {"name": "Abrar Ahmed", "role": "Middle Enforcer Spin", "perf": "+0.2033", "lub": "+0.1556", "press": "+0.2581", "se": "0.0567", "n": "776", "down": "5.4%", "rob": "8/8"},
            "alt_2": {"name": "Mitchell Santner", "role": "Middle Enforcer Spin", "perf": "+0.1215", "lub": "+0.0882", "press": "+0.1396", "se": "0.0396", "n": "1,793", "down": "12.8%", "rob": "8/8"},
            "limitations": "Smaller overall T20 delivery volume (501 balls) compared to tenured international spinners."
        },
        {
            "rank": 10, "id": 3697, "slug": "player_20_kyle_jamieson", "name": "Kyle Jamieson",
            "primary": "Powerplay Specialist (Pace)", "secondary": "Tall Strike Bowler",
            "why": "Kyle Jamieson offers an imposing physical bowling profile. Standing 6ft 8in, his steep release trajectory produces awkward bounce in powerplay conditions. Across 668 deliveries (206 pressure balls), he secures 34 wickets, an LUB20 of +0.0753, and a low blowout rate of 12.9%.",
            "best_use": "Bowling overs 1, 3, and 5 in the powerplay. Forcing rushed pull shots and defensive edges off good length.",
            "worst_use": "Bowling overs 18–20 at the death where full lengths can be cleanly targeted.",
            "failure_cond": "Batters moving out of the crease to nullify bounce and hit through the line on true wickets.",
            "alt_1": {"name": "Jamie Overton", "role": "Death/Middle Enforcer Pace", "perf": "+0.1941", "lub": "+0.1398", "press": "+0.2541", "se": "0.0645", "n": "525", "down": "17.2%", "rob": "8/8"},
            "alt_2": {"name": "Josh Hazlewood", "role": "Death/New Ball Pace", "perf": "+0.1255", "lub": "+0.0893", "press": "+0.1478", "se": "0.0430", "n": "1,515", "down": "17.7%", "rob": "8/8"},
            "limitations": "Must be protected from death-overs exposure; best utilized strictly in overs 1–12."
        }
    ]
    
    for b in bowler_metadata:
        fpath = target_dir / f"{b['slug']}.md"
        row = df_ev[(df_ev['player_id'] == b['id']) & (df_ev['role'] == 'bowler')].iloc[0]
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(f"# PinkOps Target File: {b['name']} (Bowler Rank {b['rank']})\n")
            f.write("**Project:** Operation Pink Panther / PinkOps  \n")
            f.write("**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  \n")
            f.write(f"**Target ID:** `PINKOPS-TARGET-BOWL-{b['rank']:02d}`  \n")
            f.write(f"**Player ID:** `{b['id']}`  \n")
            f.write(f"**Date:** November 2026  \n\n")
            f.write("---\n\n")
            f.write("## 1. PLAYER & ROLE PROFILE\n\n")
            f.write(f"- **Player Name:** {b['name']}\n")
            f.write(f"- **Primary Tactical Role:** {b['primary']}\n")
            f.write(f"- **Secondary Role:** {b['secondary']}\n")
            f.write(f"- **Teams in Dataset:** {row['teams']}\n")
            f.write(f"- **Competitions:** {row['competitions']} ({row['seasons']})\n")
            f.write(f"- **Evidence Tier:** {row['evidence_tier']} ({row['exposure_tier']})\n")
            f.write(f"- **Reliability Profile:** {row['reliability_profile']}\n\n")
            f.write("---\n\n")
            f.write("## 2. WHY PINKOPS SHOULD TARGET THEM\n\n")
            f.write(f"{b['why']}\n\n")
            f.write("---\n\n")
            f.write("## 3. MULTIDIMENSIONAL EVIDENCE AUDIT\n\n")
            f.write("### A. Performance Evidence (Spec B Contextual Model)\n")
            f.write(f"- **Actual Runs Conceded:** {int(row['actual_runs_conceded']):,} runs across {int(row['n_deliveries_total']):,} deliveries\n")
            f.write(f"- **Contextual Expected Runs:** {row['expected_runs_conceded']:.1f} runs (Baseline: {row['mean_expected_runs']:.3f} runs/ball)\n")
            f.write(f"- **Total Run Prevention:** **+{row['run_prevention_total']:.2f} runs saved** relative to expectation\n")
            f.write(f"- **Total Bowler Wickets:** {int(row['bowler_wickets'])} wickets (Strike Rate: {row['wicket_strike_rate']:.1f} balls/wkt)\n")
            f.write(f"- **Dot Ball Percentage:** {row['dot_ball_pct']*100:.1f}%\n")
            f.write(f"- **Boundary Conceded Rate:** {row['boundary_conceded_pct']*100:.1f}%\n\n")
            f.write("### B. Pressure Performance & Clutch Contrast\n")
            f.write(f"- **Pressure Exposure (PI >= 0.5898):** {int(row['n_deliveries_pressure']):,} deliveries ({row['pressure_ratio']*100:.1f}% of total)\n")
            f.write(f"- **Pressure Run Prevention (RVA):** **+{row['rva_per_ball_pressure']:.4f} runs/ball** under high leverage\n")
            f.write(f"- **Matched Clutch Contrast (CEM Delta):** {row['clutch_delta_rva']:+.4f} runs/ball elevation vs matched control\n")
            f.write(f"- **Dot Ball % Under Pressure:** {row['dot_pct_pressure']*100:.1f}%\n\n")
            f.write("### C. Reliability & Lower Uncertainty Bounds\n")
            f.write(f"- **Empirical Bayes Estimate (K=100):** **+{row['eb_shrunk_estimate']:.4f}**\n")
            f.write(f"- **Standard Error (SE_EB):** {row['se_eb']:.4f} ({row['uncertainty_tier']})\n")
            f.write(f"- **LUB20 (Downside Decision Floor):** **+{row['lub_20']:.4f}**\n")
            f.write(f"- **Quantile Multiverse Bounds:** LUB10: {row['lub_10']:+.4f} | LUB20: {row['lub_20']:+.4f} | LUB25: {row['lub_25']:+.4f} | LUB30: {row['lub_30']:+.4f}\n")
            f.write(f"- **Match-Level Dispersion:** MAD = {row['match_va_mad']:.4f} | IQR = {row['match_va_iqr']:.4f}\n\n")
            f.write("### D. Downside Risk Assessment\n")
            f.write(f"- **Match Blowout Rate:** **{row['pressure_collapse_rate']*100:.1f}%** (Governance Ceiling: 20.0%)\n")
            f.write(f"- **Negative Match Percentage:** {row['negative_match_pct']*100:.1f}%\n")
            f.write(f"- **Discipline Extras Rate:** {row['discipline_extras_rate']*100:.2f}% (Wides/No-balls)\n\n")
            f.write("### E. Multiverse Robustness Verification\n")
            f.write(f"- **Specifications Supported:** **{row['multiverse_specs_supported']}/8** ({row['multiverse_support_pct']:.1f}%)\n")
            f.write(f"- **Robustness Tier:** {row['robustness_tier']}\n")
            f.write(f"- **Spec A vs Spec B Stability:** Spec B LUB20 = +{row['spec_b_lub20']:.4f} vs Spec A LUB20 = +{row['spec_a_lub20']:.4f}\n\n")
            f.write("---\n\n")
            f.write("## 4. TACTICAL DEPLOYMENT BLUEPRINT\n\n")
            f.write(f"- **Best Tactical Use:** {b['best_use']}\n")
            f.write(f"- **Worst Tactical Use:** {b['worst_use']}\n")
            f.write(f"- **Primary Failure Conditions:** {b['failure_cond']}\n\n")
            f.write("---\n\n")
            f.write("## 5. COMPARABLE PLAYER ANALYSIS\n\n")
            f.write("| Candidate | Role | Contextual Run Prev | LUB20 | Pressure RVA | Uncertainty (SE) | Sample Size | Blowout Rate | Robustness Support |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
            f.write(f"| **{b['name']} (Selected)** | {b['primary']} | +{row['eb_shrunk_estimate']:.4f} | **+{row['lub_20']:.4f}** | +{row['rva_per_ball_pressure']:.4f} | {row['se_eb']:.4f} | {int(row['n_deliveries_total']):,} | {row['pressure_collapse_rate']*100:.1f}% | {row['multiverse_specs_supported']}/8 |\n")
            f.write(f"| {b['alt_1']['name']} (Alt 1) | {b['alt_1']['role']} | {b['alt_1']['perf']} | {b['alt_1']['lub']} | {b['alt_1']['press']} | {b['alt_1']['se']} | {b['alt_1']['n']} | {b['alt_1']['down']} | {b['alt_1']['rob']} |\n")
            f.write(f"| {b['alt_2']['name']} (Alt 2) | {b['alt_2']['role']} | {b['alt_2']['perf']} | {b['alt_2']['lub']} | {b['alt_2']['press']} | {b['alt_2']['se']} | {b['alt_2']['n']} | {b['alt_2']['down']} | {b['alt_2']['rob']} |\n\n")
            f.write("---\n\n")
            f.write("## 6. DATA LIMITATIONS\n\n")
            f.write(f"{b['limitations']}\n\n")
            f.write("---\n\n")
            f.write(f"*End of Target File for {b['name']}.*\n")
            
    print(f"Successfully generated all 20 Target Dossiers in {target_dir}.")

if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    generate_all_target_files(proj_root)
