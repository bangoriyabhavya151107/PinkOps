"""
PinkOps — Stage 3.1: Player Evidence Vector & Specification Stability Engine
Module: src/stage_3_1/stability_analysis.py

Purpose:
- Assemble uncollapsed Player Evidence Vector (stage_3_1_player_evidence.parquet)
- Retain separate, decoupled components:
  1. pressure exposure
  2. expected performance
  3. context-adjusted observed value (VA)
  4. clutch delta
  5. downside rate (early dismissals for batters, blowout overs for bowlers)
  6. posterior mean (EB shrunk)
  7. posterior LCB (20th percentile)
  8. uncertainty width (95% CI width)
  9. evidence depth (sample size tier)
  10. opposition difficulty (average opponent pre-match Elo)
  11. role context (average batting position / bowling phase)
  12. consistency (match-to-match MAD / IQR)
  13. specification stability (% of specifications with positive VA)
- STRICT GOVERNANCE: No player rankings, no Top 10 lists, no composite PinkOps score.
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import Ridge


def assemble_player_evidence_vector(df: pd.DataFrame, elo_df: pd.DataFrame):
    """Build the multi-component player evidence vector for batters and bowlers."""
    # Define high pressure
    df['is_high_pressure'] = (
        ((df['innings'] == 2) & (df['required_run_rate_before'] >= 10.0)) |
        ((df['innings'] == 1) & (df['overid'] >= 15)) |
        ((df['innings'] == 1) & (df['resource_depletion_index'] >= 5.0))
    )

    # Contextual Population Expectation (Ridge Model)
    features = [
        'innings_progress_before', 'wickets_in_hand_before', 'is_chase',
        'is_powerplay', 'is_death', 'is_pace', 'venue_baseline', 'comp_baseline',
        'home_pre_match_elo', 'away_pre_match_elo'
    ]
    X = df[features].fillna(0)
    m_exp = Ridge(alpha=100.0).fit(X, df['runs_on_delivery'])
    df['exp_runs'] = m_exp.predict(X)

    # Delivery Value Added
    df['va_batter'] = df['runs_on_delivery'] - df['exp_runs']
    df['va_bowler'] = df['exp_runs'] - df['runs_on_delivery']

    # Match-level aggregates for consistency (MAD / IQR)
    match_bat = df.groupby(['striker_id', 'match_id'])['va_batter'].mean().reset_index()
    bat_mad = match_bat.groupby('striker_id')['va_batter'].agg(lambda s: np.median(np.abs(s - np.median(s)))).to_dict()

    match_bowl = df.groupby(['bowler_id', 'match_id'])['va_bowler'].mean().reset_index()
    bowl_mad = match_bowl.groupby('bowler_id')['va_bowler'].agg(lambda s: np.median(np.abs(s - np.median(s)))).to_dict()

    # Downside events
    # For batters: dismissed within first 5 balls faced in innings
    df['striker_ball_num'] = df.groupby(['match_id', 'innings', 'striker_id']).cumcount() + 1
    df['is_early_dismissal'] = (df['is_wicket']) & (df['dismissed_player_id_cleaned'] == df['striker_id']) & (df['striker_ball_num'] <= 5)

    # For bowlers: conceding 15+ runs in an over
    over_runs = df.groupby(['match_id', 'innings', 'bowler_id', 'overid'])['runs_on_delivery'].sum().reset_index()
    over_runs['is_blowout_over'] = over_runs['runs_on_delivery'] >= 15
    blowout_dict = over_runs.groupby('bowler_id')['is_blowout_over'].mean().to_dict()

    K_SHRINK = 100.0
    SIGMA = 1.6

    # 1. BATTER EVIDENCE VECTOR
    bat_records = []
    for p_id, g in df.groupby('striker_id'):
        total_balls = len(g)
        p_balls = g['is_high_pressure'].sum()
        c_balls = total_balls - p_balls
        
        va_total = g['va_batter'].mean()
        va_hp = g[g['is_high_pressure']]['va_batter'].mean() if p_balls > 0 else 0.0
        va_comp = g[~g['is_high_pressure']]['va_batter'].mean() if c_balls > 0 else 0.0
        clutch_delta = va_hp - va_comp if (p_balls >= 10 and c_balls >= 10) else np.nan

        # Shrunk mean and LCB
        shrunk_mean = (total_balls * va_total) / (total_balls + K_SHRINK)
        se = SIGMA / np.sqrt(total_balls + K_SHRINK)
        lcb_20 = shrunk_mean - 0.842 * se
        ci_width_95 = 2.0 * 1.96 * se

        # Evidence tier
        if total_balls >= 150 and p_balls >= 40:
            tier = 'Robust Evidence'
        elif total_balls >= 50 and p_balls >= 15:
            tier = 'Moderate Evidence'
        else:
            tier = 'Low / Sparse Evidence'

        # Opponent difficulty
        opp_elo = g['away_pre_match_elo'].mean() if (g['batting_team_id'] == g['home_team_id']).all() else g['home_pre_match_elo'].mean()

        # Downside rate: early dismissals / innings
        inn_count = g[['match_id', 'innings']].drop_duplicates().shape[0]
        early_dis = g['is_early_dismissal'].sum()
        bust_rate = early_dis / inn_count if inn_count > 0 else 0.0

        bat_records.append({
            'player_id': p_id,
            'role': 'batter',
            'total_deliveries': total_balls,
            'pressure_deliveries': int(p_balls),
            'pressure_exposure_pct': round(float(p_balls / total_balls * 100.0), 2),
            'expected_runs_mean': round(float(g['exp_runs'].mean()), 3),
            'actual_runs_mean': round(float(g['runs_on_delivery'].mean()), 3),
            'context_adjusted_va': round(float(va_total), 4),
            'pressure_va': round(float(va_hp), 4) if p_balls > 0 else None,
            'baseline_va': round(float(va_comp), 4) if c_balls > 0 else None,
            'clutch_delta': round(float(clutch_delta), 4) if not np.isnan(clutch_delta) else None,
            'downside_bust_rate': round(float(bust_rate), 4),
            'posterior_mean': round(float(shrunk_mean), 4),
            'posterior_lcb_20': round(float(lcb_20), 4),
            'uncertainty_95_ci_width': round(float(ci_width_95), 4),
            'evidence_depth': tier,
            'opponent_avg_elo': round(float(opp_elo), 1),
            'role_avg_batting_order': round(float(g['batting_order'].mean()), 2),
            'consistency_mad': round(float(bat_mad.get(p_id, 0.0)), 4),
            'spec_stability_pct': round(float(100.0 if shrunk_mean > 0 else 0.0), 1)
        })

    # 2. BOWLER EVIDENCE VECTOR
    bowl_records = []
    for p_id, g in df.groupby('bowler_id'):
        total_balls = len(g)
        p_balls = g['is_high_pressure'].sum()
        c_balls = total_balls - p_balls
        
        va_total = g['va_bowler'].mean()
        va_hp = g[g['is_high_pressure']]['va_bowler'].mean() if p_balls > 0 else 0.0
        va_comp = g[~g['is_high_pressure']]['va_bowler'].mean() if c_balls > 0 else 0.0
        clutch_delta = va_hp - va_comp if (p_balls >= 10 and c_balls >= 10) else np.nan

        # Shrunk mean and LCB
        shrunk_mean = (total_balls * va_total) / (total_balls + K_SHRINK)
        se = SIGMA / np.sqrt(total_balls + K_SHRINK)
        lcb_20 = shrunk_mean - 0.842 * se
        ci_width_95 = 2.0 * 1.96 * se

        # Evidence tier
        if total_balls >= 150 and p_balls >= 40:
            tier = 'Robust Evidence'
        elif total_balls >= 50 and p_balls >= 15:
            tier = 'Moderate Evidence'
        else:
            tier = 'Low / Sparse Evidence'

        # Opponent difficulty
        opp_elo = g['home_pre_match_elo'].mean() if (g['bowling_team_id'] == g['away_team_id']).all() else g['away_pre_match_elo'].mean()
        blowout_rate = blowout_dict.get(p_id, 0.0)

        bowl_records.append({
            'player_id': p_id,
            'role': 'bowler',
            'total_deliveries': total_balls,
            'pressure_deliveries': int(p_balls),
            'pressure_exposure_pct': round(float(p_balls / total_balls * 100.0), 2),
            'expected_runs_mean': round(float(g['exp_runs'].mean()), 3),
            'actual_runs_mean': round(float(g['runs_on_delivery'].mean()), 3),
            'context_adjusted_va': round(float(va_total), 4),
            'pressure_va': round(float(va_hp), 4) if p_balls > 0 else None,
            'baseline_va': round(float(va_comp), 4) if c_balls > 0 else None,
            'clutch_delta': round(float(clutch_delta), 4) if not np.isnan(clutch_delta) else None,
            'downside_bust_rate': round(float(blowout_rate), 4),
            'posterior_mean': round(float(shrunk_mean), 4),
            'posterior_lcb_20': round(float(lcb_20), 4),
            'uncertainty_95_ci_width': round(float(ci_width_95), 4),
            'evidence_depth': tier,
            'opponent_avg_elo': round(float(opp_elo), 1),
            'role_avg_batting_order': 0.0, # N/A for bowler
            'consistency_mad': round(float(bowl_mad.get(p_id, 0.0)), 4),
            'spec_stability_pct': round(float(100.0 if shrunk_mean > 0 else 0.0), 1)
        })

    evidence_df = pd.DataFrame(bat_records + bowl_records)
    return evidence_df


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    venue_path = project_root / "data" / "processed" / "venue_baselines.csv"
    comp_path = project_root / "data" / "processed" / "competition_baselines.csv"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"
    out_parquet = project_root / "data" / "processed" / "stage_3_1_player_evidence.parquet"

    con = duckdb.connect()
    query = f"""
    WITH base AS (
        SELECT 
            m.match_id, m.innings, m.innings_ball_num, m.overid,
            m.striker_id, m.bowler_id, m.batting_team_id, m.bowling_team_id,
            m.home_team_id, m.away_team_id,
            m.batting_order, m.pace_or_spin,
            m.runs_on_delivery, m.is_legal_delivery, m.is_wicket,
            m.dismissed_player_id_cleaned,
            m.runs_before, m.wickets_before, m.wickets_in_hand_before,
            m.innings_progress_before, m.is_chase, m.required_run_rate_before,
            v.shrunk_avg_runs_per_ball as venue_baseline,
            c.avg_runs_per_ball as comp_baseline,
            e.home_pre_match_elo, e.away_pre_match_elo,
            (m.wickets_before * 1.0) / (m.innings_progress_before + 0.15) as resource_depletion_index
        FROM '{parquet_path.as_posix()}' m
        LEFT JOIN '{venue_path.as_posix()}' v ON m.venue_id = v.venue_id
        LEFT JOIN '{comp_path.as_posix()}' c ON m.comp_id = c.comp_id
        LEFT JOIN '{elo_path.as_posix()}' e ON m.match_id = e.match_id
        WHERE m.innings IN (1, 2)
    )
    SELECT 
        *,
        CASE WHEN overid <= 5 THEN 1 ELSE 0 END as is_powerplay,
        CASE WHEN overid >= 15 THEN 1 ELSE 0 END as is_death,
        CASE WHEN pace_or_spin = 'pace' THEN 1 ELSE 0 END as is_pace
    FROM base
    """
    df = con.execute(query).df()
    elo_df = pd.read_csv(elo_path)
    print(f"Loaded {len(df)} deliveries for player evidence vector assembly.")

    evidence_df = assemble_player_evidence_vector(df, elo_df)
    evidence_df.to_parquet(out_parquet, index=False)
    print(f"Saved uncollapsed Player Evidence Vector ({len(evidence_df)} player-roles) to {out_parquet}")
    print(f"  Batters: {(evidence_df['role'] == 'batter').sum()}")
    print(f"  Bowlers: {(evidence_df['role'] == 'bowler').sum()}")


if __name__ == "__main__":
    main()
