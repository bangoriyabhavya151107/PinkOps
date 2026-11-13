"""
PinkOps — Stage 4.1.1: Genuine Methodological Multiverse Engine (Hardened)
Module: src/stage_4_1_1/multiverse.py

Purpose:
- Rigorously recompute player reliability under genuine independent methodological specifications.
- Strictly PROHIBITS synthetic perturbations, post-hoc multipliers, or hardcoded constants (-1.30).
- Uses the CANONICAL expectation & attribution framework on all delivery recomputations:
    * Batters: VA_j = runs_j - expected_runs_j (from fitted Spec B model)
    * Bowlers: VA_j = expected_runs_j - runs_conceded_j
- Formally classifies EVERY branch as one of:
    1. FULL_RECOMPUTATION
    2. PARTIAL_RECOMPUTATION
    3. DESCRIPTOR_ALTERNATIVE
- Strictly separates:
    A. Methodological Performance Support (out of 6 genuine performance specifications)
    B. Descriptor Corroboration (auxiliary consistency & clutch descriptors)
- Exports: data/processed/stage_4_1_1_multiverse_results.csv
"""

import sys
import duckdb
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# Add project root to path
proj_root = Path(__file__).resolve().parents[2]
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

from src.stage_4_0.opportunity import compute_delivery_pressure_intensity
from src.stage_4_0.expectation import build_contextual_expectation


def run_genuine_multiverse(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    venue_path = project_root / "data" / "processed" / "venue_baselines.csv"
    comp_path = project_root / "data" / "processed" / "competition_baselines.csv"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"
    evidence_path = project_root / "data" / "processed" / "stage_4_1_player_evidence.parquet"
    out_csv = project_root / "data" / "processed" / "stage_4_1_1_multiverse_results.csv"
    
    print(f"Loading player evidence from {evidence_path}...")
    df_evidence = pd.read_parquet(evidence_path)
    
    # Restrict to qualified cohort for robustness evaluation (Robust + Moderate: >= 15 pressure balls)
    eval_df = df_evidence[df_evidence['n_deliveries_pressure'] >= 15].copy()
    n_total_eval = len(eval_df)
    n_batters = len(eval_df[eval_df['role'] == 'batter'])
    n_bowlers = len(eval_df[eval_df['role'] == 'bowler'])
    print(f"Evaluating genuine multiverse across {n_total_eval} qualified players ({n_batters} batters, {n_bowlers} bowlers)...")
    
    # Baseline Primary Specification Vector (SPEC_00)
    baseline_lub20 = eval_df['lub_20'].values
    baseline_ranks = pd.Series(baseline_lub20).rank(ascending=False).values
    top_quartile_cutoff = np.percentile(baseline_lub20, 75)
    baseline_top_quartile = set(eval_df[eval_df['lub_20'] >= top_quartile_cutoff]['player_id'])
    baseline_positive = set(eval_df[eval_df['lub_20'] > 0]['player_id'])
    
    sigma_pop = 1.10
    raw_mean = eval_df['rva_per_ball_pressure'].values
    n_press = eval_df['n_deliveries_pressure'].values
    
    multiverse_records = []
    
    def evaluate_branch(spec_id, spec_family, provenance_class, spec_desc, pert_metric, p_spec, v_k, e_k, s_k, l_spec, c_spec, cs_spec):
        pert_metric = np.nan_to_num(pert_metric, nan=0.0)
        pert_ranks = pd.Series(pert_metric).rank(ascending=False).values
        
        r_s, _ = stats.spearmanr(baseline_lub20, pert_metric)
        med_rank_chg = np.median(np.abs(pert_ranks - baseline_ranks))
        
        pert_top_q_cutoff = np.percentile(pert_metric, 75)
        pert_top_quartile = set(eval_df[pert_metric >= pert_top_q_cutoff]['player_id'])
        top_q_overlap = len(baseline_top_quartile & pert_top_quartile) / len(baseline_top_quartile) if len(baseline_top_quartile) > 0 else 1.0
        
        pert_positive = set(eval_df[pert_metric > 0]['player_id'])
        sign_stab = len(baseline_positive & pert_positive) / len(baseline_positive) if len(baseline_positive) > 0 else 1.0
        
        # Classification stability: fraction of players maintaining same sign & relative tier
        class_stab = (np.sign(baseline_lub20) == np.sign(pert_metric)).mean()
        
        multiverse_records.append({
            "spec_id": spec_id,
            "spec_family": spec_family,
            "provenance_classification": provenance_class,
            "spec_description": spec_desc,
            "pressure_spec": p_spec,
            "venue_K": v_k,
            "elo_K": e_k,
            "shrinkage_K": s_k,
            "lub_spec": l_spec,
            "clutch_spec": c_spec,
            "consistency_spec": cs_spec,
            "n_batters": n_batters,
            "n_bowlers": n_bowlers,
            "median_rank_change": round(float(med_rank_chg), 1),
            "spearman_vs_primary": round(float(r_s), 4),
            "top_quartile_overlap": round(float(top_q_overlap), 4),
            "sign_stability": round(float(sign_stab), 4),
            "classification_stability": round(float(class_stab), 4)
        })
    
    # -------------------------------------------------------------
    # SPEC_00: Canonical Primary Operating Specification
    # -------------------------------------------------------------
    evaluate_branch(
        "SPEC_00_PRIMARY", "Primary Baseline", "FULL_RECOMPUTATION",
        "Canonical Frozen Spec B (K=100, LUB20, PI80, CEM)",
        baseline_lub20, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # -------------------------------------------------------------
    # FAMILY 1: Shrinkage Strength K Variants (PARTIAL_RECOMPUTATION)
    # Recomputed directly from player delivery count n_i and sample mean Y_bar
    # -------------------------------------------------------------
    for k_val in [50.0, 200.0]:
        lam = n_press / (n_press + k_val)
        eb_k = lam * raw_mean
        se_k = np.sqrt((sigma_pop**2) / (n_press + k_val))
        lub20_k = eb_k - 0.842 * se_k
        evaluate_branch(
            f"SPEC_SHRINK_K_{int(k_val)}", "Shrinkage Multiverse", "PARTIAL_RECOMPUTATION",
            f"Recomputed Empirical Bayes with K={int(k_val)}",
            lub20_k, "PI_80 (Eps=0.15)", 500, 32, k_val, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
        )
        
    # -------------------------------------------------------------
    # FAMILY 2: Lower Uncertainty Bound Quantile Variants (PARTIAL_RECOMPUTATION)
    # -------------------------------------------------------------
    lub_quantiles = [
        ("LUB_10", 1.282, "Strict Downside (p=10, z=1.282)"),
        ("LUB_15", 1.036, "Moderate Conservative (p=15, z=1.036)"),
        ("LUB_25", 0.674, "Mild Conservative (p=25, z=0.674)"),
        ("LUB_30", 0.524, "Permissive Bound (p=30, z=0.524)")
    ]
    for l_id, z_val, l_desc in lub_quantiles:
        lub_q = eval_df['eb_shrunk_estimate'].values - z_val * eval_df['se_eb'].values
        evaluate_branch(
            f"SPEC_QUANT_{l_id}", "LUB Quantile Multiverse", "PARTIAL_RECOMPUTATION",
            f"Recomputed bound under {l_desc}",
            lub_q, "PI_80 (Eps=0.15)", 500, 32, 100.0, f"{l_id} (z={z_val})", "Multi-Dimensional CEM", "Match MAD"
        )
        
    # -------------------------------------------------------------
    # FAMILY 3: Expectation Model Specification (FULL_RECOMPUTATION)
    # Spec A Contextual Model including recent-12 deliveries micro-momentum
    # -------------------------------------------------------------
    spec_a_vals = eval_df['spec_a_lub20'].values
    evaluate_branch(
        "SPEC_EXP_SPEC_A", "Expectation Model Multiverse", "FULL_RECOMPUTATION",
        "Spec A Contextual Model (Including Recent 12 Deliveries Micro-Momentum)",
        spec_a_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # -------------------------------------------------------------
    # FAMILY 4: Consistency & Dispersion Descriptors (DESCRIPTOR_ALTERNATIVE)
    # Evaluates whether dispersion measures rank differently from mean performance
    # -------------------------------------------------------------
    iqr_vals = -1.0 * eval_df['match_va_iqr'].values
    evaluate_branch(
        "SPEC_DISP_IQR", "Consistency Multiverse", "DESCRIPTOR_ALTERNATIVE",
        "Match-Level Interquartile Range (IQR) Dispersion Descriptor",
        iqr_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match IQR"
    )
    neg_match_vals = -1.0 * eval_df['negative_match_pct'].values
    evaluate_branch(
        "SPEC_DISP_NEG_MATCH", "Consistency Multiverse", "DESCRIPTOR_ALTERNATIVE",
        "Negative Match Contribution Rate (Non-Loss Rate Descriptor)",
        neg_match_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Negative Match Rate"
    )
    
    # -------------------------------------------------------------
    # FAMILY 5: Clutch Matching Descriptors (DESCRIPTOR_ALTERNATIVE)
    # Matched relative value-added elevation Delta RVA
    # -------------------------------------------------------------
    clutch_vals = eval_df['clutch_delta_rva'].values
    evaluate_branch(
        "SPEC_CLUTCH_DELTA", "Clutch Matching Multiverse", "DESCRIPTOR_ALTERNATIVE",
        "Coarsened Exact Matched Relative Value Added (Delta RVA Descriptor)",
        clutch_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Delta RVA Matched", "Match MAD"
    )
    
    # -------------------------------------------------------------
    # FAMILY 6: Genuine Delivery Recomputation for Pressure Cutoffs (FULL_RECOMPUTATION)
    # Uses CANONICAL Expectation Model Residuals: NO HARDCODED -1.30!
    # -------------------------------------------------------------
    print("Loading match state deliveries and fitting canonical Spec B expectation model...")
    con = duckdb.connect()
    deliv_query = f"""
    WITH base AS (
        SELECT 
            m.match_id, m.innings, m.innings_ball_num, m.overid,
            m.striker_id, m.bowler_id, m.home_team_id, m.away_team_id,
            m.batting_team_id, m.bowling_team_id, m.batting_order, m.pace_or_spin,
            m.runs, m.runs_on_delivery, m.extras_type, m.is_legal_delivery,
            m.wickets_before, m.wickets_in_hand_before, m.balls_remaining_before,
            m.innings_progress_before, m.is_chase, m.runs_required_before,
            v.shrunk_avg_runs_per_ball as venue_baseline,
            c.avg_runs_per_ball as comp_baseline,
            e.home_pre_match_elo, e.away_pre_match_elo
        FROM '{parquet_path.as_posix()}' m
        LEFT JOIN '{venue_path.as_posix()}' v ON m.venue_id = v.venue_id
        LEFT JOIN '{comp_path.as_posix()}' c ON m.comp_id = c.comp_id
        LEFT JOIN '{elo_path.as_posix()}' e ON m.match_id = e.match_id
        WHERE m.is_super_over = 0 AND m.innings IN (1, 2)
    )
    SELECT *,
        CASE WHEN overid <= 5 THEN 1 ELSE 0 END as is_powerplay,
        CASE WHEN overid >= 15 THEN 1 ELSE 0 END as is_death,
        CASE WHEN LOWER(pace_or_spin) = 'pace' THEN 1 ELSE 0 END as is_pace
    FROM base
    """
    deliv_df = con.execute(deliv_query).df()
    deliv_df['batter_balls_faced_before'] = deliv_df.groupby(['match_id', 'innings', 'striker_id']).cumcount()
    
    # Fit canonical Spec B expectation model
    exp_runs, _, _ = build_contextual_expectation(deliv_df, spec='B', role_adjusted=True)
    deliv_df['expected_runs'] = exp_runs
    
    # Calculate canonical delivery value-added residuals
    # Batter: runs off bat minus expected runs
    deliv_df['bat_va'] = deliv_df['runs'] - deliv_df['expected_runs']
    # Bowler: expected runs minus bowler conceded runs (excluding byes/leg-byes)
    extras = deliv_df['extras_type'].fillna('None')
    bowler_extras_mask = extras.isin(['wide', 'Overstep', 'other'])
    bowler_runs_conceded = np.where(bowler_extras_mask, deliv_df['runs_on_delivery'], deliv_df['runs'])
    deliv_df['bowl_va'] = deliv_df['expected_runs'] - bowler_runs_conceded
    
    # Base pressure intensity with epsilon = 0.15
    deliv_df['pi_base'] = compute_delivery_pressure_intensity(deliv_df, epsilon=0.15)
    
    # 6a. Recompute at PI >= 70th percentile (FULL_RECOMPUTATION)
    cutoff_70 = np.percentile(deliv_df['pi_base'], 70)
    sub_70 = deliv_df[deliv_df['pi_base'] >= cutoff_70]
    
    bat_70 = sub_70.groupby('striker_id')['bat_va'].agg(['count', 'mean'])
    bowl_70 = sub_70.groupby('bowler_id')['bowl_va'].agg(['count', 'mean'])
    
    eval_df['n_pi70'] = np.where(
        eval_df['role'] == 'batter',
        eval_df['player_id'].map(bat_70['count']).fillna(0),
        eval_df['player_id'].map(bowl_70['count']).fillna(0)
    )
    eval_df['rva_pi70'] = np.where(
        eval_df['role'] == 'batter',
        eval_df['player_id'].map(bat_70['mean']).fillna(0.0),
        eval_df['player_id'].map(bowl_70['mean']).fillna(0.0)
    )
    lam_70 = eval_df['n_pi70'].values / (eval_df['n_pi70'].values + 100.0)
    lub20_pi70 = lam_70 * eval_df['rva_pi70'].values - 0.842 * np.sqrt((sigma_pop**2) / (eval_df['n_pi70'].values + 100.0))
    evaluate_branch(
        "SPEC_PRESS_PI70", "Pressure Cutoff Multiverse", "FULL_RECOMPUTATION",
        f"Recomputed delivery model residual aggregation at PI >= {cutoff_70:.2f} (PI_70)",
        lub20_pi70, "PI_70 (Top 30%)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # 6b. Recompute at PI >= 85th percentile (FULL_RECOMPUTATION)
    cutoff_85 = np.percentile(deliv_df['pi_base'], 85)
    sub_85 = deliv_df[deliv_df['pi_base'] >= cutoff_85]
    
    bat_85 = sub_85.groupby('striker_id')['bat_va'].agg(['count', 'mean'])
    bowl_85 = sub_85.groupby('bowler_id')['bowl_va'].agg(['count', 'mean'])
    
    eval_df['n_pi85'] = np.where(
        eval_df['role'] == 'batter',
        eval_df['player_id'].map(bat_85['count']).fillna(0),
        eval_df['player_id'].map(bowl_85['count']).fillna(0)
    )
    eval_df['rva_pi85'] = np.where(
        eval_df['role'] == 'batter',
        eval_df['player_id'].map(bat_85['mean']).fillna(0.0),
        eval_df['player_id'].map(bowl_85['mean']).fillna(0.0)
    )
    lam_85 = eval_df['n_pi85'].values / (eval_df['n_pi85'].values + 100.0)
    lub20_pi85 = lam_85 * eval_df['rva_pi85'].values - 0.842 * np.sqrt((sigma_pop**2) / (eval_df['n_pi85'].values + 100.0))
    evaluate_branch(
        "SPEC_PRESS_PI85", "Pressure Cutoff Multiverse", "FULL_RECOMPUTATION",
        f"Recomputed delivery model residual aggregation at PI >= {cutoff_85:.2f} (PI_85)",
        lub20_pi85, "PI_85 (Top 15%)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # 6c. RDI Epsilon Variants (FULL_RECOMPUTATION)
    for eps in [0.10, 0.20]:
        pi_eps = compute_delivery_pressure_intensity(deliv_df, epsilon=eps)
        cutoff_eps = np.percentile(pi_eps, 80)
        sub_eps = deliv_df[pi_eps >= cutoff_eps]
        
        bat_eps = sub_eps.groupby('striker_id')['bat_va'].agg(['count', 'mean'])
        bowl_eps = sub_eps.groupby('bowler_id')['bowl_va'].agg(['count', 'mean'])
        
        n_col = np.where(
            eval_df['role'] == 'batter',
            eval_df['player_id'].map(bat_eps['count']).fillna(0),
            eval_df['player_id'].map(bowl_eps['count']).fillna(0)
        )
        rva_col = np.where(
            eval_df['role'] == 'batter',
            eval_df['player_id'].map(bat_eps['mean']).fillna(0.0),
            eval_df['player_id'].map(bowl_eps['mean']).fillna(0.0)
        )
        lam_eps = n_col / (n_col + 100.0)
        lub20_eps = lam_eps * rva_col - 0.842 * np.sqrt((sigma_pop**2) / (n_col + 100.0))
        evaluate_branch(
            f"SPEC_EPS_{int(eps*100)}", "RDI Epsilon Multiverse", "FULL_RECOMPUTATION",
            f"Recomputed delivery model residuals with RDI epsilon={eps:.2f}",
            lub20_eps, f"PI_80 (Eps={eps:.2f})", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
        )
        
    # Save Machine-Readable Multiverse Results
    df_multiverse = pd.DataFrame(multiverse_records)
    df_multiverse.to_csv(out_csv, index=False)
    print(f"\nSaved hardened multiverse results to {out_csv}")
    print(df_multiverse[['spec_id', 'spec_family', 'provenance_classification', 'spearman_vs_primary', 'top_quartile_overlap', 'sign_stability', 'classification_stability']].to_string(index=False))
    
    # -------------------------------------------------------------
    # 7. Disentangled Player Evaluation:
    # A. Methodological Performance Support (out of 6 genuine performance specifications)
    # B. Descriptor Corroboration (auxiliary descriptors)
    # -------------------------------------------------------------
    perf_specs = [
        baseline_lub20,                                                      # 1. Canonical Spec B LUB20 (K=100)
        spec_a_vals,                                                         # 2. Spec A LUB20 (K=100)
        (n_press / (n_press + 50.0)) * raw_mean - 0.842 * np.sqrt(sigma_pop**2 / (n_press + 50.0)),  # 3. Shrinkage K=50
        (n_press / (n_press + 200.0)) * raw_mean - 0.842 * np.sqrt(sigma_pop**2 / (n_press + 200.0)), # 4. Shrinkage K=200
        lub20_pi70,                                                          # 5. Delivery PI_70 Cutoff
        lub20_pi85                                                           # 6. Delivery PI_85 Cutoff
    ]
    perf_matrix = np.column_stack(perf_specs)  # Shape: (n_eval, 6)
    eval_df['perf_specs_supported'] = (perf_matrix > 0).sum(axis=1)
    eval_df['perf_support_pct'] = round(eval_df['perf_specs_supported'] / 6.0 * 100.0, 1)
    
    # Auxiliary Descriptor Corroboration
    mad_threshold = np.where(eval_df['role'] == 'batter', 0.55, 0.45)
    eval_df['consistency_corroborated'] = (eval_df['match_va_mad'] <= mad_threshold).astype(int)
    eval_df['clutch_corroborated'] = (eval_df['clutch_delta_rva'] >= 0.0).astype(int)
    
    print("\n--- Methodological Performance Support Distribution (out of 6 genuine performance specifications) ---")
    print(eval_df['perf_specs_supported'].value_counts().sort_index(ascending=False))
    
    print("\n--- Auxiliary Descriptor Corroboration Summary ---")
    print(f"Consistency Corroborated (MAD <= threshold): {eval_df['consistency_corroborated'].sum()} / {len(eval_df)} ({eval_df['consistency_corroborated'].mean()*100:.1f}%)")
    print(f"Clutch Corroborated (Delta RVA >= 0):       {eval_df['clutch_corroborated'].sum()} / {len(eval_df)} ({eval_df['clutch_corroborated'].mean()*100:.1f}%)")
    
    return df_multiverse, eval_df


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_genuine_multiverse(proj_root)
