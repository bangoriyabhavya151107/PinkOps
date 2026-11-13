"""
PinkOps — Stage 4.1: Evidence Profiles Module
Module: src/stage_4_1/evidence_profiles.py

Purpose:
- Assemble the authoritative 33-dimensional uncollapsed Player Evidence Vector
  for Batters and Bowlers across all seven architectural layers.
- Uses remediated attribution, strengthened clutch matching, and Lower Uncertainty Bounds.
- Strictly enforces anti-collapse invariant: ZERO composite scores or rankings.
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path

from src.stage_4_0 import opportunity
from src.stage_4_0 import expectation
from src.stage_4_0 import attribution
from src.stage_4_0 import downside
from src.stage_4_0 import consistency
from src.stage_4_0 import clutch
from src.stage_4_0 import uncertainty


def build_player_evidence_profiles(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    venue_path = project_root / "data" / "processed" / "venue_baselines.csv"
    comp_path = project_root / "data" / "processed" / "competition_baselines.csv"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"

    con = duckdb.connect()
    
    # 1. Load normal-innings deliveries (200,961 deliveries)
    query = f"""
    WITH base AS (
        SELECT 
            m.match_id, m.innings, m.innings_ball_num, m.overid,
            m.striker_id, m.striker_name, m.non_striker_id, m.non_striker_name,
            m.bowler_id, m.bowler_name,
            m.batting_team_id, m.bowling_team_id,
            m.home_team_id, m.away_team_id,
            m.batting_order, m.pace_or_spin,
            m.runs, m.runs_on_delivery, m.extras_type, m.extras1_runs, m.extras_2_runs,
            m.is_legal_delivery, m.is_four, m.is_six, m.is_wicket,
            m.is_bowler_wicket, m.is_team_wicket, m.is_retired_hurt,
            m.dismissal_type_cleaned, m.dismissed_player_id_cleaned,
            m.runs_before, m.wickets_before, m.wickets_in_hand_before,
            m.balls_remaining_before, m.scheduled_overs,
            m.innings_progress_before,
            m.is_chase, m.runs_required_before, m.required_run_rate_before,
            v.shrunk_avg_runs_per_ball as venue_baseline,
            c.avg_runs_per_ball as comp_baseline,
            e.home_pre_match_elo, e.away_pre_match_elo,
            (m.wickets_before * 1.0) / (m.innings_progress_before + 0.15) as resource_depletion_index,
            (m.innings_progress_before * 165.0) - m.runs_before as trajectory_deficit,
            CASE WHEN m.is_chase THEN (m.runs_required_before * 1.0) / (m.balls_remaining_before + 1.0) ELSE 0 END as target_proximity,
            COALESCE(SUM(m.runs_on_delivery) OVER (
                PARTITION BY m.match_id, m.innings 
                ORDER BY m.innings_ball_num 
                ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING
            ), 0) as recent_runs_12,
            COALESCE(SUM(CASE WHEN m.is_wicket THEN 1 ELSE 0 END) OVER (
                PARTITION BY m.match_id, m.innings 
                ORDER BY m.innings_ball_num 
                ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING
            ), 0) as recent_wickets_12,
            COALESCE(SUM(CASE WHEN m.runs_on_delivery = 0 THEN 1 ELSE 0 END) OVER (
                PARTITION BY m.match_id, m.innings 
                ORDER BY m.innings_ball_num 
                ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING
            ), 0) as recent_dots_12
        FROM '{parquet_path.as_posix()}' m
        LEFT JOIN '{venue_path.as_posix()}' v ON m.venue_id = v.venue_id
        LEFT JOIN '{comp_path.as_posix()}' c ON m.comp_id = c.comp_id
        LEFT JOIN '{elo_path.as_posix()}' e ON m.match_id = e.match_id
        WHERE m.innings IN (1, 2)
    )
    SELECT 
        *,
        CASE WHEN overid <= 5 THEN 'Powerplay' WHEN overid >= 15 THEN 'Death' ELSE 'Middle' END as phase,
        CASE WHEN overid <= 5 THEN 1 ELSE 0 END as is_powerplay,
        CASE WHEN overid >= 15 THEN 1 ELSE 0 END as is_death,
        CASE WHEN LOWER(pace_or_spin) = 'pace' THEN 1 ELSE 0 END as is_pace
    FROM base
    """
    df = con.execute(query).df()
    print(f"Loaded {len(df):,} normal-innings deliveries across 1st and 2nd innings.")
    
    # Cumulative balls faced by striker in innings
    df['batter_balls_faced_before'] = df.groupby(['match_id', 'innings', 'striker_id']).cumcount()
    
    # 2. Layer 1: Opportunity Layer
    df = opportunity.build_pressure_opportunity(df, epsilon=0.15)
    
    # 3. Layer 2: Expectation Layer (Frozen Specification B & Sensitivity Spec A)
    exp_runs_b, model_b, feats_b = expectation.build_contextual_expectation(df, spec='B', role_adjusted=True)
    df['expected_runs'] = exp_runs_b
    
    exp_runs_a, model_a, feats_a = expectation.build_contextual_expectation(df, spec='A', role_adjusted=True)
    df['expected_runs_spec_a'] = exp_runs_a
    
    # 4. Layer 3: Execution Layer (Remediated Attribution)
    df = attribution.compute_delivery_va(df, exp_col='expected_runs')
    df['va_batter_spec_a'] = df['bat_runs_attributed'] - df['expected_runs_spec_a']
    df['va_bowler_spec_a'] = df['expected_runs_spec_a'] - df['bowler_runs_conceded']
    
    # 5. Layer 4, 5, 6 for Batters
    print("Computing multi-layer evidence components for Batters...")
    bat_names = df.groupby('striker_id')['striker_name'].last().to_dict()
    bat_exp = opportunity.aggregate_player_exposure(df, role='batter')
    bat_attr = attribution.calculate_player_va(df, role='batter')
    bat_down = downside.calculate_downside_metrics(df, role='batter')
    bat_cons = consistency.calculate_consistency(df, role='batter')
    bat_clutch = clutch.calculate_clutch_delta(df, role='batter')
    bat_unc = uncertainty.estimate_uncertainty(bat_attr, value_col='pressure_va_per_ball', sample_col='pressure_deliveries', k_shrink=100.0)
    
    # Opponent Elo
    df['opp_elo_batter'] = np.where(df['batting_team_id'] == df['home_team_id'], df['away_pre_match_elo'], df['home_pre_match_elo'])
    df['opp_elo_bowler'] = np.where(df['bowling_team_id'] == df['home_team_id'], df['away_pre_match_elo'], df['home_pre_match_elo'])
    
    bat_context = df.groupby('striker_id').agg(
        pct_powerplay=('is_powerplay', 'mean'),
        pct_death=('is_death', 'mean'),
        pct_vs_pace=('is_pace', 'mean'),
        mean_opp_elo_faced=('opp_elo_batter', 'mean')
    ).reset_index().rename(columns={'striker_id': 'player_id'})
    
    bat_spec_a_means = df[df['is_high_pressure'] == 1].groupby('striker_id')['va_batter_spec_a'].mean().to_dict()
    
    # 6. Layer 4, 5, 6 for Bowlers
    print("Computing multi-layer evidence components for Bowlers...")
    bowl_names = df.groupby('bowler_id')['bowler_name'].last().to_dict()
    bowl_exp = opportunity.aggregate_player_exposure(df, role='bowler')
    bowl_attr = attribution.calculate_player_va(df, role='bowler')
    bowl_down = downside.calculate_downside_metrics(df, role='bowler')
    bowl_cons = consistency.calculate_consistency(df, role='bowler')
    bowl_clutch = clutch.calculate_clutch_delta(df, role='bowler')
    bowl_unc = uncertainty.estimate_uncertainty(bowl_attr, value_col='pressure_va_per_ball', sample_col='pressure_deliveries', k_shrink=100.0)
    
    bowl_context = df.groupby('bowler_id').agg(
        pct_powerplay=('is_powerplay', 'mean'),
        pct_death=('is_death', 'mean'),
        pct_vs_pace=('is_pace', 'mean'),
        mean_opp_elo_faced=('opp_elo_bowler', 'mean')
    ).reset_index().rename(columns={'bowler_id': 'player_id'})
    
    bowl_spec_a_means = df[df['is_high_pressure'] == 1].groupby('bowler_id')['va_bowler_spec_a'].mean().to_dict()
    
    # Super Over context
    so_query = f"""
        SELECT 
            striker_id, bowler_id, COUNT(*) as cnt
        FROM '{parquet_path.as_posix()}'
        WHERE innings IN (3, 4)
        GROUP BY striker_id, bowler_id
    """
    so_df = con.execute(so_query).df()
    so_bat = so_df.groupby('striker_id')['cnt'].sum().to_dict()
    so_bowl = so_df.groupby('bowler_id')['cnt'].sum().to_dict()
    
    # 7. Assemble Unified Evidence Vectors
    # Batters Vector
    bat_rows = []
    for p_id in bat_exp['player_id']:
        name = bat_names.get(p_id, f"Batter_{p_id}")
        exp_row = bat_exp[bat_exp['player_id'] == p_id].iloc[0]
        attr_row = bat_attr[bat_attr['player_id'] == p_id].iloc[0]
        down_row = bat_down[bat_down['player_id'] == p_id].iloc[0] if p_id in bat_down['player_id'].values else None
        cons_row = bat_cons[bat_cons['player_id'] == p_id].iloc[0] if p_id in bat_cons['player_id'].values else None
        clutch_row = bat_clutch[bat_clutch['player_id'] == p_id].iloc[0] if p_id in bat_clutch['player_id'].values else None
        unc_row = bat_unc[bat_unc['player_id'] == p_id].iloc[0]
        ctx_row = bat_context[bat_context['player_id'] == p_id].iloc[0] if p_id in bat_context['player_id'].values else None
        
        n_tot = int(exp_row['total_opportunities'])
        n_pr = int(exp_row['pressure_opportunities'])
        pr_ratio = n_pr / n_tot if n_tot > 0 else 0.0
        
        spec_a_raw = bat_spec_a_means.get(p_id, 0.0)
        w_pr = n_pr / (n_pr + 100.0)
        spec_a_eb = w_pr * spec_a_raw
        spec_a_lub20 = spec_a_eb - 0.842 * unc_row['se_eb']
        
        bat_rows.append({
            'player_id': p_id,
            'player_name': name,
            'role': 'batter',
            # Layer 1: Opportunity
            'n_deliveries_total': n_tot,
            'n_deliveries_pressure': n_pr,
            'pressure_ratio': round(float(pr_ratio), 4),
            'weighted_pressure_exposure': round(float(exp_row['weighted_pressure_exposure']), 4),
            'mean_pressure_faced': round(float(exp_row['mean_pressure_intensity']), 4),
            # Layer 2: Expectation
            'mean_expected_runs': round(float(attr_row['expected_performance_mean']), 4),
            'mean_expected_runs_pressure': round(float(df[(df['striker_id'] == p_id) & (df['is_high_pressure'] == 1)]['expected_runs'].mean()), 4) if n_pr > 0 else 0.0,
            # Layer 3: Execution
            'rva_per_ball_pressure': round(float(attr_row['pressure_va_per_ball']), 4),
            'boundary_pct_pressure': round(float(attr_row['boundary_execution_rate']), 4),
            'dot_pct_pressure': round(float(attr_row['dot_execution_rate']), 4),
            'strike_rate_pressure': round(float(df[(df['striker_id'] == p_id) & (df['is_high_pressure'] == 1)]['bat_runs_attributed'].sum() / n_pr * 100.0), 2) if n_pr > 0 else 0.0,
            # Layer 4: Downside & Consistency
            'early_dismissal_rate': round(float(down_row['early_dismissal_rate']), 4) if down_row is not None else 0.0,
            'pressure_collapse_rate': round(float(down_row['pressure_collapse_rate']), 4) if down_row is not None else 0.0,
            'match_va_mad': round(float(cons_row['consistency_mad']), 4) if cons_row is not None else 0.0,
            'match_va_iqr': round(float(cons_row['consistency_iqr']), 4) if cons_row is not None else 0.0,
            'negative_match_pct': round(float(cons_row['negative_match_pct'] / 100.0), 4) if cons_row is not None else 0.0,
            # Layer 4: Clutch
            'clutch_delta_rva': round(float(clutch_row['clutch_delta_matched']), 4) if (clutch_row is not None and clutch_row['clutch_delta_matched'] is not None) else 0.0,
            # Layer 5: Uncertainty (Remediated LUB)
            'eb_shrunk_estimate': round(float(unc_row['eb_shrunk_estimate']), 4),
            'se_eb': round(float(unc_row['se_eb']), 4),
            'lub_10': round(float(unc_row['lub_10']), 4),
            'lub_20': round(float(unc_row['lub_20']), 4),
            'lub_25': round(float(unc_row['lub_25']), 4),
            'lub_30': round(float(unc_row['lub_30']), 4),
            'lcb_20': round(float(unc_row['lub_20']), 4), # Alias
            # Layer 6: Context
            'evidence_tier': exp_row['evidence_tier'],
            'pct_powerplay': round(float(ctx_row['pct_powerplay']), 4) if ctx_row is not None else 0.0,
            'pct_death': round(float(ctx_row['pct_death']), 4) if ctx_row is not None else 0.0,
            'pct_vs_pace': round(float(ctx_row['pct_vs_pace']), 4) if ctx_row is not None else 0.0,
            'mean_opp_elo_faced': round(float(ctx_row['mean_opp_elo_faced']), 1) if ctx_row is not None else 1500.0,
            'super_over_balls': int(so_bat.get(p_id, 0)),
            # Layer 7: Decision Sensitivity
            'spec_b_lub20': round(float(unc_row['lub_20']), 4),
            'spec_a_lub20': round(float(spec_a_lub20), 4)
        })
    df_bat_evidence = pd.DataFrame(bat_rows)
    
    # Bowlers Vector
    bowl_rows = []
    for p_id in bowl_exp['player_id']:
        name = bowl_names.get(p_id, f"Bowler_{p_id}")
        exp_row = bowl_exp[bowl_exp['player_id'] == p_id].iloc[0]
        attr_row = bowl_attr[bowl_attr['player_id'] == p_id].iloc[0]
        down_row = bowl_down[bowl_down['player_id'] == p_id].iloc[0] if p_id in bowl_down['player_id'].values else None
        cons_row = bowl_cons[bowl_cons['player_id'] == p_id].iloc[0] if p_id in bowl_cons['player_id'].values else None
        clutch_row = bowl_clutch[bowl_clutch['player_id'] == p_id].iloc[0] if p_id in bowl_clutch['player_id'].values else None
        unc_row = bowl_unc[bowl_unc['player_id'] == p_id].iloc[0]
        ctx_row = bowl_context[bowl_context['player_id'] == p_id].iloc[0] if p_id in bowl_context['player_id'].values else None
        
        n_tot = int(exp_row['total_opportunities'])
        n_pr = int(exp_row['pressure_opportunities'])
        pr_ratio = n_pr / n_tot if n_tot > 0 else 0.0
        
        spec_a_raw = bowl_spec_a_means.get(p_id, 0.0)
        w_pr = n_pr / (n_pr + 100.0)
        spec_a_eb = w_pr * spec_a_raw
        spec_a_lub20 = spec_a_eb - 0.842 * unc_row['se_eb']
        
        bowl_rows.append({
            'player_id': p_id,
            'player_name': name,
            'role': 'bowler',
            # Layer 1: Opportunity
            'n_deliveries_total': n_tot,
            'n_deliveries_pressure': n_pr,
            'pressure_ratio': round(float(pr_ratio), 4),
            'weighted_pressure_exposure': round(float(exp_row['weighted_pressure_exposure']), 4),
            'mean_pressure_faced': round(float(exp_row['mean_pressure_intensity']), 4),
            # Layer 2: Expectation
            'mean_expected_runs': round(float(attr_row['expected_performance_mean']), 4),
            'mean_expected_runs_pressure': round(float(df[(df['bowler_id'] == p_id) & (df['is_high_pressure'] == 1)]['expected_runs'].mean()), 4) if n_pr > 0 else 0.0,
            # Layer 3: Execution
            'rva_per_ball_pressure': round(float(attr_row['pressure_va_per_ball']), 4), # RCS stored here
            'boundary_pct_pressure': round(float(attr_row['boundary_execution_rate']), 4),
            'dot_pct_pressure': round(float(attr_row['dot_execution_rate']), 4),
            'strike_rate_pressure': round(float(df[(df['bowler_id'] == p_id) & (df['is_high_pressure'] == 1)]['bowler_runs_conceded'].sum() / (n_pr / 6.0)), 2) if n_pr >= 6 else 0.0,
            # Layer 4: Downside & Consistency
            'early_dismissal_rate': round(float(down_row['blowout_over_rate']), 4) if down_row is not None else 0.0,
            'pressure_collapse_rate': round(float(down_row['death_failure_rate']), 4) if down_row is not None else 0.0,
            'match_va_mad': round(float(cons_row['consistency_mad']), 4) if cons_row is not None else 0.0,
            'match_va_iqr': round(float(cons_row['consistency_iqr']), 4) if cons_row is not None else 0.0,
            'negative_match_pct': round(float(cons_row['negative_match_pct'] / 100.0), 4) if cons_row is not None else 0.0,
            # Layer 4: Clutch
            'clutch_delta_rva': round(float(clutch_row['clutch_delta_matched']), 4) if (clutch_row is not None and clutch_row['clutch_delta_matched'] is not None) else 0.0,
            # Layer 5: Uncertainty (Remediated LUB)
            'eb_shrunk_estimate': round(float(unc_row['eb_shrunk_estimate']), 4),
            'se_eb': round(float(unc_row['se_eb']), 4),
            'lub_10': round(float(unc_row['lub_10']), 4),
            'lub_20': round(float(unc_row['lub_20']), 4),
            'lub_25': round(float(unc_row['lub_25']), 4),
            'lub_30': round(float(unc_row['lub_30']), 4),
            'lcb_20': round(float(unc_row['lub_20']), 4), # Alias
            # Layer 6: Context
            'evidence_tier': exp_row['evidence_tier'],
            'pct_powerplay': round(float(ctx_row['pct_powerplay']), 4) if ctx_row is not None else 0.0,
            'pct_death': round(float(ctx_row['pct_death']), 4) if ctx_row is not None else 0.0,
            'pct_vs_pace': round(float(ctx_row['pct_vs_pace']), 4) if ctx_row is not None else 0.0,
            'mean_opp_elo_faced': round(float(ctx_row['mean_opp_elo_faced']), 1) if ctx_row is not None else 1500.0,
            'super_over_balls': int(so_bowl.get(p_id, 0)),
            # Layer 7: Decision Sensitivity
            'spec_b_lub20': round(float(unc_row['lub_20']), 4),
            'spec_a_lub20': round(float(spec_a_lub20), 4)
        })
    df_bowl_evidence = pd.DataFrame(bowl_rows)
    
    df_unified = pd.concat([df_bat_evidence, df_bowl_evidence], ignore_index=True)
    print(f"Assembled Unified Evidence Vector: {len(df_bat_evidence)} batters, {len(df_bowl_evidence)} bowlers (Total: {len(df_unified)}).")
    
    return df_bat_evidence, df_bowl_evidence, df_unified
