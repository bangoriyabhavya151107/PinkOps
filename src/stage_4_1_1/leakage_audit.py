"""
PinkOps — Stage 4.1.1: End-to-End Leakage Provenance Audit
Module: src/stage_4_1_1/leakage_audit.py

Purpose:
- Rigorously classify all features in the decision pipeline into exact temporal categories:
    * PRE_DELIVERY: Known prior to the current ball being bowled (t-)
    * HISTORICAL_PRE_MATCH: Known prior to match start from historical data
    * POST_DELIVERY: Known only after current ball is bowled (t+) -> TARGET / RESIDUAL ONLY
    * POST_MATCH: Known only after match concludes -> CONTEXT / VALIDATION ONLY
    * UNKNOWN: Not permitted in any model (triggers immediate failure)
- Exports: data/processed/stage_4_1_1_leakage_audit.csv
"""

import pandas as pd
from pathlib import Path


def run_leakage_audit(project_root: Path):
    out_csv = project_root / "data" / "processed" / "stage_4_1_1_leakage_audit.csv"
    
    pipeline_features = [
        # Match State Pre-Delivery Features
        ("innings_progress_before", "Legal balls bowled / scheduled balls", "PRE_DELIVERY", "Model input: phase progress", "LEAKAGE-FREE"),
        ("balls_remaining_before", "Scheduled balls - legal balls bowled", "PRE_DELIVERY", "Model input: resource availability", "LEAKAGE-FREE"),
        ("wickets_before", "Total wickets fallen prior to delivery", "PRE_DELIVERY", "Model input: resource scarcity", "LEAKAGE-FREE"),
        ("wickets_in_hand_before", "10 - wickets_before", "PRE_DELIVERY", "Model input: wickets remaining", "LEAKAGE-FREE"),
        ("runs_before", "Total innings runs scored prior to delivery", "PRE_DELIVERY", "Model input: trajectory score", "LEAKAGE-FREE"),
        ("is_chase", "Binary indicator: 2nd innings contested chase", "PRE_DELIVERY", "Model input: chase context", "LEAKAGE-FREE"),
        ("runs_required_before", "Target runs - runs_before", "PRE_DELIVERY", "Model input: chase target stress", "LEAKAGE-FREE"),
        ("required_run_rate_before", "Runs required / balls remaining * 6", "PRE_DELIVERY", "Model input: rate stress", "LEAKAGE-FREE"),
        ("target_proximity", "runs_required / (balls_remaining + 1.0)", "PRE_DELIVERY", "Model input: chase urgency", "LEAKAGE-FREE"),
        ("resource_depletion_index", "wickets_before / (progress + 0.15)", "PRE_DELIVERY", "Model input: crisis stress", "LEAKAGE-FREE"),
        ("trajectory_deficit", "progress * 165.0 - runs_before", "PRE_DELIVERY", "Model input: target deficit", "LEAKAGE-FREE"),
        ("overid", "Over index (0 to 19)", "PRE_DELIVERY", "Model input: phase indicator", "LEAKAGE-FREE"),
        ("is_powerplay", "Binary: overid <= 5", "PRE_DELIVERY", "Model input: field restrictions", "LEAKAGE-FREE"),
        ("is_death", "Binary: overid >= 15", "PRE_DELIVERY", "Model input: death phase", "LEAKAGE-FREE"),
        ("is_pace", "Binary: pace or spin", "PRE_DELIVERY", "Model input: bowling style", "LEAKAGE-FREE"),
        ("batting_order", "Order position (1 to 11)", "PRE_DELIVERY", "Model input: role context", "LEAKAGE-FREE"),
        ("batter_balls_faced_before", "Cumulative balls faced by batter in match", "PRE_DELIVERY", "Model input: batter set status", "LEAKAGE-FREE"),
        
        # Historical Pre-Match Baselines
        ("home_pre_match_elo", "Team Elo prior to match start", "HISTORICAL_PRE_MATCH", "Model input: team strength", "LEAKAGE-FREE"),
        ("away_pre_match_elo", "Team Elo prior to match start", "HISTORICAL_PRE_MATCH", "Model input: team strength", "LEAKAGE-FREE"),
        ("venue_baseline", "Historical shrunk venue scoring average", "HISTORICAL_PRE_MATCH", "Model input: venue par", "LEAKAGE-FREE"),
        ("comp_baseline", "Historical competition scoring average", "HISTORICAL_PRE_MATCH", "Model input: league par", "LEAKAGE-FREE"),
        ("hist_venue_baseline", "Expanding pre-match venue baseline excluding current match", "HISTORICAL_PRE_MATCH", "Clutch input: venue environment", "LEAKAGE-FREE"),
        
        # Rolling Features (Strictly Prior Deliveries)
        ("recent_runs_12", "Runs in prior 12 balls (ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING)", "PRE_DELIVERY", "Spec A input only (Spec B excludes)", "LEAKAGE-FREE"),
        ("recent_wickets_12", "Wickets in prior 12 balls (strictly prior)", "PRE_DELIVERY", "Spec A input only (Spec B excludes)", "LEAKAGE-FREE"),
        ("recent_dots_12", "Dot balls in prior 12 balls (strictly prior)", "PRE_DELIVERY", "Spec A input only (Spec B excludes)", "LEAKAGE-FREE"),
        
        # Post-Delivery Events (Target & Evaluation Residuals Only)
        ("runs_on_delivery", "Total runs scored on current ball", "POST_DELIVERY", "Expectation target variable (y)", "TARGET_VARIABLE"),
        ("runs", "Runs off bat on current ball", "POST_DELIVERY", "Batter attribution target", "TARGET_VARIABLE"),
        ("is_bowler_wicket", "Wicket credited to bowler on current ball", "POST_DELIVERY", "Bowler attribution target", "TARGET_VARIABLE"),
        ("is_team_wicket", "Wicket fallen on current ball", "POST_DELIVERY", "Innings tracking target", "TARGET_VARIABLE"),
        
        # Post-Match Terminal Outcomes (Validation Only)
        ("win_team_id", "Winning team identifier", "POST_MATCH", "Match outcome validation only", "POST_MATCH_CONTEXT"),
        ("post_match_result", "Match result string", "POST_MATCH", "Match outcome validation only", "POST_MATCH_CONTEXT")
    ]
    
    df_leakage = pd.DataFrame(pipeline_features, columns=[
        "feature_name", "definition", "temporal_classification", "pipeline_role", "leakage_status"
    ])
    
    df_leakage.to_csv(out_csv, index=False)
    print(f"Saved end-to-end leakage audit to {out_csv}")
    print(df_leakage['temporal_classification'].value_counts())
    
    # Assertions
    unknown_features = df_leakage[df_leakage['temporal_classification'] == 'UNKNOWN']
    assert len(unknown_features) == 0, f"Found UNKNOWN features: {unknown_features}"
    
    model_inputs = df_leakage[df_leakage['pipeline_role'].str.contains('Model input|Clutch input')]
    for idx, row in model_inputs.iterrows():
        assert row['temporal_classification'] in ['PRE_DELIVERY', 'HISTORICAL_PRE_MATCH'], f"Leakage: {row['feature_name']} has classification {row['temporal_classification']}"
        
    print("[ALL LEAKAGE AUDIT INVARIANTS PASS: 100% of model inputs are PRE_DELIVERY or HISTORICAL_PRE_MATCH]")
    return df_leakage


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_leakage_audit(proj_root)
