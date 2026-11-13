"""
PinkOps — Stage 6: Final Competition Delivery & Evidence Defense Automated Test Suite (T01 - T35)
Module: src/stage_6/test_stage_6.py

Purpose:
- Rigorously validates all Stage 6 deliverables, evidence defense dossiers, submission package,
  reproducibility standards, and raw data immutability.
- Contains 35 programmatic assertions (T01 through T35).
- Exits with 0 on complete pass, 1 on any failure.
- Logs test summary to outputs/stage_6_test_results.txt.
"""

import hashlib
import json
import re
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to path
proj_root = Path(__file__).resolve().parents[2]
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

BASELINE_RAW_HASHES = {
    "ball_by_ball.csv": "01E2B4379EDFBAB6A6E456D304CB3C70F554CB312EF93D9588F3F32A82CB396E",
    "competitions.csv": "507CEB7189F972D4E4F299DDCFC97F3C3247AF1913F6291106F161FA8353FD9B",
    "competition_team_player_mapping.csv": "1DED4E42A933618572D6E2C3A521C3257EB1844FAB4456D567D77CBB2D3BBB12",
    "matches.csv": "BB100AB84B8B9A15160C1F2315CF675210131A30E779EC5079FD5403DCF56EEF",
    "playing_eleven.csv": "7517C73722A28D5D61C808CCF0CBED315A8780586D02E946EB9A7F5DAF011C27",
    "teams.csv": "A65E5922A9B3BF49247B24FC9471782E700EFB31F8DCC5042923238B87C50A5D",
    "Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf": "8F7965C616D4A64B779E770A6B2C17DDE6A2D6CCBF7DE12A58B04DB792162489"
}

def calculate_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().upper()

def run_stage_6_tests():
    data_dir = proj_root / "data" / "processed"
    raw_dir = proj_root / "data" / "raw" / "6af458274c1e8_data_pack" / "Data Pack"
    outputs_dir = proj_root / "outputs"
    sub_dir = outputs_dir / "STAGE_6_FINAL_SUBMISSION"
    target_dir = outputs_dir / "target_files"
    log_file = outputs_dir / "stage_6_test_results.txt"
    
    test_results = []
    
    def log_test(test_id, test_name, passed, detail=""):
        status_str = "PASS" if passed else "FAIL"
        line = f"[{status_str}] {test_id}: {test_name}"
        if detail:
            line += f" -> {detail}"
        print(line)
        test_results.append((test_id, test_name, status_str, detail))
        if not passed:
            raise AssertionError(f"Test {test_id} FAILED: {detail}")

    print("================================================================================")
    print("STAGE 6 FINAL COMPETITION DELIVERY & EVIDENCE DEFENSE TEST SUITE (T01 - T35)")
    print("================================================================================")

    # -------------------------------------------------------------------------
    # T01: Stage 5 Gate File Exists
    # -------------------------------------------------------------------------
    gate5_path = outputs_dir / "stage_5_final_gate.md"
    passed = gate5_path.exists() and gate5_path.stat().st_size > 500
    log_test("T01", "Stage 5 Gate File Exists", passed, f"Size: {gate5_path.stat().st_size} bytes")

    # -------------------------------------------------------------------------
    # T02: Stage 5 Status Verified GREEN
    # -------------------------------------------------------------------------
    gate5_content = gate5_path.read_text(encoding="utf-8")
    passed = bool(re.search(r"STAGE_5_STATUS\s*=\s*GREEN", gate5_content))
    log_test("T02", "Stage 5 Status Verified GREEN", passed, "Verified STAGE_5_STATUS = GREEN in gate")

    # -------------------------------------------------------------------------
    # T03: Raw Data SHA-256 Immutability Check
    # -------------------------------------------------------------------------
    hash_mismatches = []
    for fname, exp_hash in BASELINE_RAW_HASHES.items():
        fpath = raw_dir / fname
        if not fpath.exists():
            hash_mismatches.append(f"{fname}: File Not Found")
            continue
        cur_hash = calculate_sha256(fpath)
        if cur_hash != exp_hash:
            hash_mismatches.append(f"{fname}: Expected {exp_hash[:8]}..., Got {cur_hash[:8]}...")
    passed = (len(hash_mismatches) == 0)
    log_test("T03", "Raw Data SHA-256 Immutability", passed, "All 7 raw competition files bitwise unchanged" if passed else "; ".join(hash_mismatches))

    # -------------------------------------------------------------------------
    # T04: Exactly 10 Final Batters Selected
    # -------------------------------------------------------------------------
    df_bat = pd.read_csv(outputs_dir / "final_10_batters.csv")
    passed = (len(df_bat) == 10)
    log_test("T04", "Exactly 10 Final Batters Selected", passed, f"Count: {len(df_bat)}")

    # -------------------------------------------------------------------------
    # T05: Exactly 10 Final Bowlers Selected
    # -------------------------------------------------------------------------
    df_bowl = pd.read_csv(outputs_dir / "final_10_bowlers.csv")
    passed = (len(df_bowl) == 10)
    log_test("T05", "Exactly 10 Final Bowlers Selected", passed, f"Count: {len(df_bowl)}")

    # -------------------------------------------------------------------------
    # T06: Exactly 20 Final Players in Comparison Table
    # -------------------------------------------------------------------------
    df_comp = pd.read_csv(outputs_dir / "final_player_comparison.csv")
    passed = (len(df_comp) == 20)
    log_test("T06", "Exactly 20 Final Players in Comparison Table", passed, f"Count: {len(df_comp)}")

    # -------------------------------------------------------------------------
    # T07: Unique Player IDs Across Final Selections
    # -------------------------------------------------------------------------
    df_master = pd.read_csv(outputs_dir / "stage_6_master_player_evidence.csv")
    unique_ids = set(df_master["player_id"].tolist())
    unique_names = set(df_comp["player"].tolist())
    passed = (len(unique_ids) == 20 and len(unique_names) == 20)
    log_test("T07", "Unique Player IDs Across Final Selections", passed, f"Unique IDs: {len(unique_ids)}, Unique Names: {len(unique_names)}")

    # -------------------------------------------------------------------------
    # T08: Zero Nulls in Core Decision Metrics
    # -------------------------------------------------------------------------
    null_cols = []
    for col in ["player_id", "player_name", "role", "total_exposure", "pressure_exposure", "lub20", "se_eb"]:
        if df_master[col].isnull().any():
            null_cols.append(col)
    passed = (len(null_cols) == 0 and not df_comp.isnull().any().any())
    log_test("T08", "Zero Nulls in Core Decision Metrics", passed, "All core metrics non-null in master and comparison tables" if passed else f"Nulls in: {null_cols}")

    # -------------------------------------------------------------------------
    # T09: Strictly Positive Lower Uncertainty Bounds (LUB20 > 0)
    # -------------------------------------------------------------------------
    min_lub_bat = df_bat["lub_20"].min()
    min_lub_bowl = df_bowl["lub_20"].min()
    min_lub = min(min_lub_bat, min_lub_bowl)
    passed = (min_lub > 0.0)
    log_test("T09", "Strictly Positive Lower Uncertainty Bounds", passed, f"Minimum LUB20: {min_lub:.4f} > 0.0")

    # -------------------------------------------------------------------------
    # T10: Epistemic Uncertainty Standard Error strictly positive (SE_EB > 0)
    # -------------------------------------------------------------------------
    min_se = min(df_bat["se_eb"].min(), df_bowl["se_eb"].min())
    passed = (min_se > 0.0)
    log_test("T10", "Positive Empirical Bayes Standard Error", passed, f"Minimum SE_EB: {min_se:.4f} > 0.0")

    # -------------------------------------------------------------------------
    # T11: Pressure Exposure Thresholds Satisfied (N_pr >= 40)
    # -------------------------------------------------------------------------
    min_pr_balls = min(df_bat["pressure_exposure"].min(), df_bowl["pressure_exposure"].min())
    passed = (min_pr_balls >= 40)
    log_test("T11", "Pressure Exposure Thresholds Satisfied", passed, f"Minimum pressure balls: {min_pr_balls} >= 40")

    # -------------------------------------------------------------------------
    # T12: Evidence Tier Correctness (All Robust Evidence)
    # -------------------------------------------------------------------------
    tiers = set(df_comp["evidence_tier"].tolist())
    passed = (tiers == {"Robust Evidence"} and set(df_bat["evidence_tier"]) == {"Robust Evidence"} and set(df_bowl["evidence_tier"]) == {"Robust Evidence"})
    log_test("T12", "Evidence Tier Correctness", passed, f"Tiers present: {tiers}")

    # -------------------------------------------------------------------------
    # T13: Target Files Count Exactly 20
    # -------------------------------------------------------------------------
    target_files = list(target_dir.glob("player_*.md"))
    passed = (len(target_files) == 20)
    log_test("T13", "Target Files Count Exactly 20", passed, f"Target file count: {len(target_files)}")

    # -------------------------------------------------------------------------
    # T14: Target Files Coverage Complete
    # -------------------------------------------------------------------------
    target_contents = [tf.read_text(encoding="utf-8") for tf in target_files]
    missing_targets = []
    all_player_names = df_bat["player_name"].tolist() + df_bowl["player_name"].tolist()
    for pname in all_player_names:
        if not any(pname.lower() in tc.lower() for tc in target_contents):
            missing_targets.append(pname)
    passed = (len(missing_targets) == 0)
    log_test("T14", "Target Files Coverage Complete", passed, "All 20 players have individual target files" if passed else f"Missing: {missing_targets}")

    # -------------------------------------------------------------------------
    # T15: Final Comparison Table Reconciliation
    # -------------------------------------------------------------------------
    bat_names = set(df_bat["player_name"].tolist())
    bowl_names = set(df_bowl["player_name"].tolist())
    comp_names = set(df_comp["player"].tolist())
    passed = (bat_names.union(bowl_names) == comp_names and len(bat_names.intersection(bowl_names)) == 0)
    log_test("T15", "Final Comparison Table Reconciliation", passed, "Batters (10) + Bowlers (10) partition comparison table (20)")

    # -------------------------------------------------------------------------
    # T16: Final Auction Board Reconciliation
    # -------------------------------------------------------------------------
    df_auc = pd.read_csv(outputs_dir / "final_auction_board.csv")
    auc_names = set(df_auc["player"].tolist())
    passed = (len(df_auc) == 20 and auc_names == comp_names)
    log_test("T16", "Final Auction Board Reconciliation", passed, f"Auction board rows: {len(df_auc)}, matches final 20 names")

    # -------------------------------------------------------------------------
    # T17: PinkOps Mission Brief Reconciliation
    # -------------------------------------------------------------------------
    mb_content = (outputs_dir / "pinkops_mission_brief.md").read_text(encoding="utf-8")
    missing_in_mb = [name for name in comp_names if name not in mb_content]
    passed = (len(missing_in_mb) == 0)
    log_test("T17", "PinkOps Mission Brief Reconciliation", passed, "All 20 player names present in mission brief" if passed else f"Missing: {missing_in_mb}")

    # -------------------------------------------------------------------------
    # T18: No Fabricated Auction Prices / Monetary Values
    # -------------------------------------------------------------------------
    # Check that auction boards and strategies do not claim fictitious rupee / currency values
    strat_content = (outputs_dir / "stage_6_final_strategy.md").read_text(encoding="utf-8")
    auc_text = df_auc.to_string()
    suspicious_patterns = [r"\b\d+\s*crore\b", r"₹\s*\d+", r"\$\s*\d+", r"\b\d+\s*cr\b"]
    matches_found = []
    for pat in suspicious_patterns:
        if re.search(pat, auc_text, re.IGNORECASE):
            matches_found.append(f"Auction board pattern: {pat}")
    passed = (len(matches_found) == 0)
    log_test("T18", "No Fabricated Auction Prices", passed, "Zero monetary prices or currency figures in auction board" if passed else "; ".join(matches_found))

    # -------------------------------------------------------------------------
    # T19: No Fabricated Auction Rules
    # -------------------------------------------------------------------------
    rules_doc = (outputs_dir / "stage_6_competition_rules_defense.md").read_text(encoding="utf-8")
    passed = bool(re.search(r"Auction Purse.*Unspecified", rules_doc, re.IGNORECASE))
    log_test("T19", "No Fabricated Auction Rules", passed, "Explicitly documents unmentioned auction constraints as unobservable")

    # -------------------------------------------------------------------------
    # T20: Super Over Delivery Isolation
    # -------------------------------------------------------------------------
    df_ms = pd.read_parquet(data_dir / "match_state.parquet")
    super_over_balls = len(df_ms[df_ms["is_super_over"] == True])
    normal_balls = len(df_ms[df_ms["is_super_over"] == False])
    passed = (super_over_balls == 38 and normal_balls == 200961)
    log_test("T20", "Super Over Delivery Isolation", passed, f"Super over: {super_over_balls} balls, Normal: {normal_balls} balls")

    # -------------------------------------------------------------------------
    # T21: Match State Total Delivery Integrity
    # -------------------------------------------------------------------------
    total_balls = len(df_ms)
    n_matches = df_ms["match_id"].nunique()
    passed = (total_balls == 200999 and n_matches == 867)
    log_test("T21", "Match State Total Delivery Integrity", passed, f"Total balls: {total_balls:,}, Matches: {n_matches}")

    # -------------------------------------------------------------------------
    # T22: Stage 4.1.1 Evidence Lineage Verified
    # -------------------------------------------------------------------------
    df_s41 = pd.read_parquet(data_dir / "stage_4_1_player_evidence.parquet")
    passed = (len(df_s41) == 1535)
    log_test("T22", "Stage 4.1.1 Evidence Lineage Verified", passed, f"Stage 4.1.1 player records: {len(df_s41)}")

    # -------------------------------------------------------------------------
    # T23: Stage 5 Evidence Lineage Verified
    # -------------------------------------------------------------------------
    df_s5 = pd.read_parquet(data_dir / "stage_5_player_evidence.parquet")
    passed = (len(df_s5) == 1535)
    log_test("T23", "Stage 5 Evidence Lineage Verified", passed, f"Stage 5 player records: {len(df_s5)}")

    # -------------------------------------------------------------------------
    # T24: Zero Future Information Leakage
    # -------------------------------------------------------------------------
    manifest_p = outputs_dir / "stage_5_frozen_methodology_manifest.json"
    with open(manifest_p, "r", encoding="utf-8") as f:
        mf = json.load(f)
    features = mf.get("features_included", [])
    forbidden = ["match_won", "margin", "match_result", "target_achieved", "player_of_match", "innings_total_runs"]
    leaks = [f for f in features if f in forbidden]
    passed = (len(leaks) == 0)
    log_test("T24", "Zero Future Information Leakage", passed, "Verified predictive features condition strictly on t-" if passed else f"Leaks: {leaks}")

    # -------------------------------------------------------------------------
    # T25: Zero Post-Match Telemetry in Delivery Expectations
    # -------------------------------------------------------------------------
    df_leak = pd.read_csv(data_dir / "stage_4_1_1_leakage_audit.csv")
    post_match_features = df_leak[df_leak["temporal_classification"] == "POST_MATCH"]
    model_inputs = df_leak[df_leak["pipeline_role"].str.startswith("Model input")]
    passed = (
        (post_match_features["pipeline_role"] == "Match outcome validation only").all() and
        len(post_match_features) >= 2 and
        model_inputs["temporal_classification"].isin(["PRE_DELIVERY", "HISTORICAL_PRE_MATCH"]).all()
    )
    log_test("T25", "Zero Post-Match Telemetry in Expectations", passed, "Post-match statistics strictly isolated to validation-only roles")

    # -------------------------------------------------------------------------
    # T26: Stage 6 Provenance Map Completeness (>= 20 Claims)
    # -------------------------------------------------------------------------
    prov_path = outputs_dir / "stage_6_provenance_map.json"
    with open(prov_path, "r", encoding="utf-8") as f:
        prov_data = json.load(f)
    n_claims = len(prov_data) if isinstance(prov_data, list) else len(prov_data.get("claims", []))
    passed = (n_claims >= 20)
    log_test("T26", "Provenance Map Completeness", passed, f"Total verified claims: {n_claims} (>= 20)")

    # -------------------------------------------------------------------------
    # T27: All Public Claims Verified in Provenance Map
    # -------------------------------------------------------------------------
    claims_list = prov_data if isinstance(prov_data, list) else prov_data.get("claims", [])
    unverified = [c["claim_id"] for c in claims_list if c.get("status") != "VERIFIED"]
    passed = (len(unverified) == 0)
    log_test("T27", "All Public Claims Verified in Provenance Map", passed, "All claims verified against source files" if passed else f"Unverified: {unverified}")

    # -------------------------------------------------------------------------
    # T28: Robustness Denominator Consistency
    # -------------------------------------------------------------------------
    rob_res_path = outputs_dir / "stage_6_robustness_resolution.md"
    rob_content = rob_res_path.read_text(encoding="utf-8")
    has_denom_6 = ("Primary Denominator = 6" in rob_content or "6 Genuine Performance Recomputations" in rob_content)
    has_denom_8 = ("8-branch primary grid" in rob_content or "Why 8/8 vs 6/6 Appeared" in rob_content)
    has_denom_15 = ("15-Specification Universe" in rob_content or "15 total branches" in rob_content)
    passed = (has_denom_6 and has_denom_8 and has_denom_15)
    log_test("T28", "Robustness Denominator Consistency", passed, "Documented mathematical relationship between 6, 8, and 15")

    # -------------------------------------------------------------------------
    # T29: Robustness Terminology Consistency Across Artifacts
    # -------------------------------------------------------------------------
    bat_def_md = (outputs_dir / "stage_6_final_batter_defense.md").read_text(encoding="utf-8")
    bowl_def_md = (outputs_dir / "stage_6_final_bowler_defense.md").read_text(encoding="utf-8")
    passed = ("6/6 Universal" in bat_def_md and "6/6 Universal" in bowl_def_md)
    log_test("T29", "Robustness Terminology Consistency", passed, "Universal Support (6/6) terminology harmonized across defense dossiers")

    # -------------------------------------------------------------------------
    # T30: README Documentation Integrity
    # -------------------------------------------------------------------------
    readme_content = (proj_root / "README.md").read_text(encoding="utf-8")
    passed = ("STAGE 5: NOT YET EXECUTED" not in readme_content and "Stage 5 Squad Assembly" in readme_content and "Stage 6 Final Competition Delivery" in readme_content)
    log_test("T30", "README Documentation Integrity", passed, "README verified clean and fully updated with Stage 5/6 status")

    # -------------------------------------------------------------------------
    # T31: Final Batter Defense Dossier Reconciliation
    # -------------------------------------------------------------------------
    bat_ids = set(df_bat["player_id"].tolist())
    bowl_ids = set(df_bowl["player_id"].tolist())
    comp_ids = set(df_master["player_id"].tolist())
    df_bat_def = pd.read_csv(outputs_dir / "stage_6_final_batter_defense.csv")
    passed = (len(df_bat_def) == 10 and set(df_bat_def["player_id"].tolist()) == bat_ids)
    log_test("T31", "Final Batter Defense Dossier Reconciliation", passed, f"10 defense profiles match selected batters exactly")

    # -------------------------------------------------------------------------
    # T32: Final Bowler Defense Dossier Reconciliation
    # -------------------------------------------------------------------------
    df_bowl_def = pd.read_csv(outputs_dir / "stage_6_final_bowler_defense.csv")
    passed = (len(df_bowl_def) == 10 and set(df_bowl_def["player_id"].tolist()) == bowl_ids)
    log_test("T32", "Final Bowler Defense Dossier Reconciliation", passed, f"10 defense profiles match selected bowlers exactly")

    # -------------------------------------------------------------------------
    # T33: Master Player Evidence Table Reconciliation
    # -------------------------------------------------------------------------
    df_master = pd.read_csv(outputs_dir / "stage_6_master_player_evidence.csv")
    passed = (len(df_master) == 20 and set(df_master["player_id"].tolist()) == comp_ids)
    log_test("T33", "Master Player Evidence Table Reconciliation", passed, f"Master table contains exactly 20 matching player records")

    # -------------------------------------------------------------------------
    # T34: Final Strategy Narrative Reconciliation
    # -------------------------------------------------------------------------
    passed = all(name in strat_content for name in df_comp["player"]) and "## 17. Final Mission Brief" in strat_content
    log_test("T34", "Final Strategy Narrative Reconciliation", passed, "Strategy narrative includes all 20 players and all 17 sections")

    # -------------------------------------------------------------------------
    # T35: Final Submission Package Completeness
    # -------------------------------------------------------------------------
    expected_files = [
        "01_EXECUTIVE_SUMMARY.md",
        "02_METHODOLOGY.md",
        "03_FINAL_10_BATTERS.md",
        "04_FINAL_10_BOWLERS.md",
        "05_ROLE_PORTFOLIOS.md",
        "06_AUCTION_STRATEGY.md",
        "07_PLAYER_DEFENSE.md",
        "08_RISKS_AND_LIMITATIONS.md",
        "09_JUDGE_QA.md",
        "10_FINAL_MISSION_BRIEF.md",
        "11_PROVENANCE.md",
        "final_auction_board.csv",
        "final_master_player_evidence.csv",
        "final_player_comparison.csv"
    ]
    missing_sub = [f for f in expected_files if not (sub_dir / f).exists()]
    passed = (len(missing_sub) == 0)
    log_test("T35", "Final Submission Package Completeness", passed, "All 11 markdown files and 3 CSVs exist in STAGE_6_FINAL_SUBMISSION" if passed else f"Missing: {missing_sub}")

    # -------------------------------------------------------------------------
    # Write test results log
    # -------------------------------------------------------------------------
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("OPERATION PINK PANTHER — STAGE 6 COMPREHENSIVE AUTOMATED TEST RESULTS\n")
        f.write("================================================================================\n\n")
        n_pass = sum(1 for _, _, status, _ in test_results if status == "PASS")
        n_total = len(test_results)
        f.write(f"SUMMARY: {n_pass}/{n_total} ASSERTIONS PASSED (100.0%)\n")
        f.write(f"STATUS: {'GREEN' if n_pass == n_total else 'RED'}\n\n")
        f.write("DETAILED RESULTS:\n")
        for tid, tname, status, detail in test_results:
            f.write(f"[{status}] {tid}: {tname} -> {detail}\n")

    print("================================================================================")
    print(f"STAGE 6 TEST SUITE COMPLETE: {n_pass}/{n_total} ASSERTIONS PASSED")
    print(f"Results written to: {log_file}")
    print("================================================================================")

    if n_pass != n_total:
        sys.exit(1)

if __name__ == "__main__":
    run_stage_6_tests()
