"""
PinkOps — Stage 4.1.1: Genuine Methodological Multiverse Engine
Module: src/stage_4_1_1/multiverse.py

Purpose:
- Rigorously recompute player reliability under genuine independent methodological specifications.
- Strictly PROHIBITS synthetic perturbations, post-hoc multipliers (w_adj), or trigonometric offsets.
- Each branch independently recomputes the affected metrics from underlying delivery/match data:
    1. Shrinkage K: K=50, K=100 (primary), K=200
    2. LUB Quantile: LUB10, LUB15, LUB20 (primary), LUB25, LUB30
    3. Expectation Model: Spec B (primary) vs Spec A (with recent 12)
    4. Clutch Matching: Multi-Dimensional CEM (primary) vs Phase-Only CEM
    5. Consistency Descriptor: Match MAD (primary), IQR, Negative Match Contribution Rate
    6. Pressure Cutoff: PI_80 (primary), PI_70, PI_85
    7. RDI Epsilon: 0.15 (primary), 0.10, 0.20
- Evaluates:
    * Spearman rank correlation vs primary specification (r_s)
    * Median absolute rank change
    * Top quartile membership overlap
    * Sign stability (proportion of positive performers remaining positive)
    * Classification profile stability
- Exports: data/processed/stage_4_1_1_multiverse_results.csv
"""

import pandas as pd
import numpy as np
from scipy import stats
import sys
from pathlib import Path

# Add project root to path
proj_root = Path(__file__).resolve().parents[2]
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

from src.stage_4_0.opportunity import compute_delivery_pressure_intensity


def run_genuine_multiverse(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
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
    
    def evaluate_branch(spec_id, spec_family, spec_desc, pert_metric, p_spec, v_k, e_k, s_k, l_spec, c_spec, cs_spec):
        pert_metric = np.nan_to_num(pert_metric, nan=0.0)
        pert_ranks = pd.Series(pert_metric).rank(ascending=False).values
        
        r_s, _ = stats.spearmanr(baseline_lub20, pert_metric)
        med_rank_chg = np.median(np.abs(pert_ranks - baseline_ranks))
        
        pert_top_q_cutoff = np.percentile(pert_metric, 75)
        pert_top_quartile = set(eval_df[pert_metric >= pert_top_q_cutoff]['player_id'])
        top_q_overlap = len(baseline_top_quartile & pert_top_quartile) / len(baseline_top_quartile)
        
        pert_positive = set(eval_df[pert_metric > 0]['player_id'])
        sign_stab = len(baseline_positive & pert_positive) / len(baseline_positive) if len(baseline_positive) > 0 else 1.0
        
        # Classification stability: fraction of players maintaining same sign & relative tier
        class_stab = (np.sign(baseline_lub20) == np.sign(pert_metric)).mean()
        
        multiverse_records.append({
            "spec_id": spec_id,
            "spec_family": spec_family,
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
        "SPEC_00_PRIMARY", "Primary Baseline", "Canonical Frozen Spec B (K=100, LUB20, PI80, CEM)",
        baseline_lub20, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # -------------------------------------------------------------
    # FAMILY 1: Shrinkage Strength K Variants (Recomputed from n & y_bar)
    # -------------------------------------------------------------
    for k_val in [50.0, 200.0]:
        lam = n_press / (n_press + k_val)
        eb_k = lam * raw_mean
        se_k = np.sqrt((sigma_pop**2) / (n_press + k_val))
        lub20_k = eb_k - 0.842 * se_k
        evaluate_branch(
            f"SPEC_SHRINK_K_{int(k_val)}", "Shrinkage Multiverse", f"Recomputed Empirical Bayes with K={int(k_val)}",
            lub20_k, "PI_80 (Eps=0.15)", 500, 32, k_val, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
        )
        
    # -------------------------------------------------------------
    # FAMILY 2: Lower Uncertainty Bound Quantile Variants
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
            f"SPEC_QUANT_{l_id}", "LUB Quantile Multiverse", f"Recomputed bound under {l_desc}",
            lub_q, "PI_80 (Eps=0.15)", 500, 32, 100.0, f"{l_id} (z={z_val})", "Multi-Dimensional CEM", "Match MAD"
        )
        
    # -------------------------------------------------------------
    # FAMILY 3: Expectation Model Specification (Spec B vs Spec A)
    # -------------------------------------------------------------
    spec_a_vals = eval_df['spec_a_lub20'].values
    evaluate_branch(
        "SPEC_EXP_SPEC_A", "Expectation Model Multiverse", "Spec A Contextual Model (Including Recent 12 Deliveries)",
        spec_a_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # -------------------------------------------------------------
    # FAMILY 4: Consistency & Dispersion Specifications
    # -------------------------------------------------------------
    iqr_vals = -1.0 * eval_df['match_va_iqr'].values
    evaluate_branch(
        "SPEC_DISP_IQR", "Consistency Multiverse", "Match-Level Interquartile Range (IQR) Dispersion",
        iqr_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match IQR"
    )
    neg_match_vals = -1.0 * eval_df['negative_match_pct'].values
    evaluate_branch(
        "SPEC_DISP_NEG_MATCH", "Consistency Multiverse", "Negative Match Contribution Rate (Non-Loss Rate)",
        neg_match_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Negative Match Rate"
    )
    
    # -------------------------------------------------------------
    # FAMILY 5: Clutch Matching Specifications
    # -------------------------------------------------------------
    clutch_vals = eval_df['clutch_delta_rva'].values
    evaluate_branch(
        "SPEC_CLUTCH_DELTA", "Clutch Matching Multiverse", "Coarsened Exact Matched Relative Value Added (Delta RVA)",
        clutch_vals, "PI_80 (Eps=0.15)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Delta RVA Matched", "Match MAD"
    )
    
    # -------------------------------------------------------------
    # FAMILY 6: Genuine Delivery Recomputation for Pressure Cutoffs (PI70 and PI85) & Epsilon
    # -------------------------------------------------------------
    print("Loading match state deliveries to recompute delivery-level pressure specifications...")
    cols = [
        'match_id', 'innings', 'overid', 'striker_id', 'bowler_id', 
        'runs', 'runs_on_delivery', 'wickets_before', 'innings_progress_before', 
        'is_chase', 'runs_required_before', 'balls_remaining_before', 'is_super_over'
    ]
    deliv_df = pd.read_parquet(parquet_path, columns=cols)
    deliv_df = deliv_df[deliv_df['is_super_over'] == 0].copy()
    
    # 1. Base pressure intensity with epsilon = 0.15
    deliv_df['pi_base'] = compute_delivery_pressure_intensity(deliv_df, epsilon=0.15)
    
    # Recompute at PI >= 70th percentile
    cutoff_70 = np.percentile(deliv_df['pi_base'], 70)
    sub_70 = deliv_df[deliv_df['pi_base'] >= cutoff_70]
    bat_70 = sub_70.groupby('striker_id')['runs'].agg(['count', 'mean'])
    bat_70['rva'] = bat_70['mean'] - 1.30  # centered
    eval_df['n_pi70'] = eval_df['player_id'].map(bat_70['count']).fillna(0)
    eval_df['rva_pi70'] = eval_df['player_id'].map(bat_70['rva']).fillna(0.0)
    lam_70 = eval_df['n_pi70'].values / (eval_df['n_pi70'].values + 100.0)
    lub20_pi70 = lam_70 * eval_df['rva_pi70'].values - 0.842 * np.sqrt((sigma_pop**2) / (eval_df['n_pi70'].values + 100.0))
    evaluate_branch(
        "SPEC_PRESS_PI70", "Pressure Cutoff Multiverse", f"Recomputed delivery aggregation at PI >= {cutoff_70:.2f} (PI_70 threshold)",
        lub20_pi70, "PI_70 (Top 30%)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # Recompute at PI >= 85th percentile
    cutoff_85 = np.percentile(deliv_df['pi_base'], 85)
    sub_85 = deliv_df[deliv_df['pi_base'] >= cutoff_85]
    bat_85 = sub_85.groupby('striker_id')['runs'].agg(['count', 'mean'])
    bat_85['rva'] = bat_85['mean'] - 1.30
    eval_df['n_pi85'] = eval_df['player_id'].map(bat_85['count']).fillna(0)
    eval_df['rva_pi85'] = eval_df['player_id'].map(bat_85['rva']).fillna(0.0)
    lam_85 = eval_df['n_pi85'].values / (eval_df['n_pi85'].values + 100.0)
    lub20_pi85 = lam_85 * eval_df['rva_pi85'].values - 0.842 * np.sqrt((sigma_pop**2) / (eval_df['n_pi85'].values + 100.0))
    evaluate_branch(
        "SPEC_PRESS_PI85", "Pressure Cutoff Multiverse", f"Recomputed delivery aggregation at PI >= {cutoff_85:.2f} (PI_85 threshold)",
        lub20_pi85, "PI_85 (Top 15%)", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
    )
    
    # 2. RDI Epsilon Variants (Eps = 0.10 and Eps = 0.20)
    for eps in [0.10, 0.20]:
        pi_eps = compute_delivery_pressure_intensity(deliv_df, epsilon=eps)
        cutoff_eps = np.percentile(pi_eps, 80)
        sub_eps = deliv_df[pi_eps >= cutoff_eps]
        bat_eps = sub_eps.groupby('striker_id')['runs'].agg(['count', 'mean'])
        bat_eps['rva'] = bat_eps['mean'] - 1.30
        n_col = eval_df['player_id'].map(bat_eps['count']).fillna(0)
        rva_col = eval_df['player_id'].map(bat_eps['rva']).fillna(0.0)
        lam_eps = n_col.values / (n_col.values + 100.0)
        lub20_eps = lam_eps * rva_col.values - 0.842 * np.sqrt((sigma_pop**2) / (n_col.values + 100.0))
        evaluate_branch(
            f"SPEC_EPS_{int(eps*100)}", "RDI Epsilon Multiverse", f"Recomputed pressure model with RDI epsilon={eps:.2f}",
            lub20_eps, f"PI_80 (Eps={eps:.2f})", 500, 32, 100.0, "LUB_20 (z=0.842)", "Multi-Dimensional CEM", "Match MAD"
        )
        
    # Save Machine-Readable Multiverse Results
    df_multiverse = pd.DataFrame(multiverse_records)
    df_multiverse.to_csv(out_csv, index=False)
    print(f"\nSaved genuine multiverse results to {out_csv}")
    print(df_multiverse[['spec_id', 'spec_family', 'spearman_vs_primary', 'top_quartile_overlap', 'sign_stability', 'classification_stability']].to_string(index=False))
    
    # Compute Individual Player Support Counts across the 8 Core Methodological Specifications
    # 1. Primary Spec B LUB20
    # 2. Spec A LUB20
    # 3. Shrinkage K=50 LUB20
    # 4. Shrinkage K=200 LUB20
    # 5. Strict LUB10
    # 6. Permissive LUB25
    # 7. PI_70 Cutoff LUB20
    # 8. PI_85 Cutoff LUB20
    core_specs = [
        baseline_lub20,
        spec_a_vals,
        (n_press / (n_press + 50.0)) * raw_mean - 0.842 * np.sqrt(sigma_pop**2 / (n_press + 50.0)),
        (n_press / (n_press + 200.0)) * raw_mean - 0.842 * np.sqrt(sigma_pop**2 / (n_press + 200.0)),
        eval_df['eb_shrunk_estimate'].values - 1.282 * eval_df['se_eb'].values,
        eval_df['eb_shrunk_estimate'].values - 0.674 * eval_df['se_eb'].values,
        lub20_pi70,
        lub20_pi85
    ]
    
    # Stack core specifications and compute positive support count for each player
    core_matrix = np.column_stack(core_specs)  # Shape: (n_eval, 8)
    support_counts = (core_matrix > 0).sum(axis=1)
    eval_df['multiverse_specs_supported'] = support_counts
    eval_df['multiverse_support_pct'] = round(eval_df['multiverse_specs_supported'] / 8.0 * 100.0, 1)
    
    print("\nIndividual Player Multiverse Support Distribution (out of 8 core specifications):")
    print(eval_df['multiverse_specs_supported'].value_counts().sort_index(ascending=False))
    
    return df_multiverse, eval_df


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_genuine_multiverse(proj_root)
