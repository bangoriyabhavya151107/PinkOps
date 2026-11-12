"""
PinkOps — Stage 3.1: Role Confounding & Context Adjustment Engine
Module: src/stage_3_1/role_adjustment.py

Purpose:
- Control for role confounding (batting order, balls consumed, bowling phase)
- Quantify shift from raw situational VA to role-adjusted VA
- Output data/processed/stage_3_1_role_adjustment.csv
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import Ridge


def perform_role_adjustment(df: pd.DataFrame):
    """
    Fits:
    1. Raw situational expectation
    2. Role-adjusted contextual expectation
    Computes player-level shift and correlation.
    """
    # Batting balls faced before delivery by striker in innings
    df['batter_balls_faced_before'] = df.groupby(['match_id', 'innings', 'striker_id']).cumcount()

    # 1. Raw Situational Model
    X_raw = df[['innings_progress_before', 'wickets_in_hand_before', 'is_chase', 'venue_baseline', 'comp_baseline']].copy()
    X_raw['is_chase'] = X_raw['is_chase'].astype(int)
    m_raw = Ridge(alpha=100.0).fit(X_raw.fillna(0), df['runs_on_delivery'])
    df['exp_raw'] = m_raw.predict(X_raw.fillna(0))
    df['va_raw_batter'] = df['runs_on_delivery'] - df['exp_raw']

    # 2. Role-Adjusted Model (adds batting position, balls faced before, phase, pace/spin, elos)
    X_role = df[['innings_progress_before', 'wickets_in_hand_before', 'is_chase', 
                 'venue_baseline', 'comp_baseline', 'batting_order', 'batter_balls_faced_before',
                 'is_powerplay', 'is_death', 'is_pace', 'home_pre_match_elo', 'away_pre_match_elo']].copy()
    X_role['batting_order'] = X_role['batting_order'].fillna(5)
    X_role['is_chase'] = X_role['is_chase'].astype(int)

    m_role = Ridge(alpha=100.0).fit(X_role.fillna(0), df['runs_on_delivery'])
    df['exp_role'] = m_role.predict(X_role.fillna(0))
    df['va_role_batter'] = df['runs_on_delivery'] - df['exp_role']

    # Bowler Value Added (expected conceded - actual conceded)
    df['va_raw_bowler'] = df['exp_raw'] - df['runs_on_delivery']
    df['va_role_bowler'] = df['exp_role'] - df['runs_on_delivery']

    # Batter aggregation (players with >= 50 balls)
    bat_agg = df.groupby('striker_id').agg(
        balls=('runs_on_delivery', 'count'),
        avg_order=('batting_order', 'mean'),
        avg_balls_faced=('batter_balls_faced_before', 'mean'),
        death_balls=('is_death', 'sum'),
        raw_va_per_ball=('va_raw_batter', 'mean'),
        role_adj_va_per_ball=('va_role_batter', 'mean')
    ).reset_index().rename(columns={'striker_id': 'player_id'})
    bat_agg['role'] = 'batter'
    bat_agg['va_shift'] = bat_agg['role_adj_va_per_ball'] - bat_agg['raw_va_per_ball']

    # Bowler aggregation (players with >= 50 balls)
    bowl_agg = df.groupby('bowler_id').agg(
        balls=('runs_on_delivery', 'count'),
        avg_order=('batting_order', lambda x: 0.0), # N/A for bowler
        avg_balls_faced=('batter_balls_faced_before', lambda x: 0.0),
        death_balls=('is_death', 'sum'),
        raw_va_per_ball=('va_raw_bowler', 'mean'),
        role_adj_va_per_ball=('va_role_bowler', 'mean')
    ).reset_index().rename(columns={'bowler_id': 'player_id'})
    bowl_agg['role'] = 'bowler'
    bowl_agg['va_shift'] = bowl_agg['role_adj_va_per_ball'] - bowl_agg['raw_va_per_ball']

    combined = pd.concat([bat_agg, bowl_agg], ignore_index=True)
    return combined, df


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    venue_path = project_root / "data" / "processed" / "venue_baselines.csv"
    comp_path = project_root / "data" / "processed" / "competition_baselines.csv"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"
    out_csv = project_root / "data" / "processed" / "stage_3_1_role_adjustment.csv"

    con = duckdb.connect()
    query = f"""
    WITH base AS (
        SELECT 
            m.match_id, m.innings, m.innings_ball_num, m.overid,
            m.striker_id, m.bowler_id, m.batting_order, m.pace_or_spin,
            m.runs_on_delivery, m.is_legal_delivery, m.is_wicket,
            m.runs_before, m.wickets_before, m.wickets_in_hand_before,
            m.innings_progress_before, m.is_chase,
            v.shrunk_avg_runs_per_ball as venue_baseline,
            c.avg_runs_per_ball as comp_baseline,
            e.home_pre_match_elo, e.away_pre_match_elo
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
    print(f"Loaded {len(df)} deliveries for role confounding audit.")

    role_df, _ = perform_role_adjustment(df)
    role_df.round(4).to_csv(out_csv, index=False)
    print(f"Saved role adjustment summary for {len(role_df)} player-roles to {out_csv}")

    # Display diagnostics for batters with >= 100 balls
    qual = role_df[(role_df['role'] == 'batter') & (role_df['balls'] >= 100)]
    print(f"\nQualified Batters (>= 100 balls): {len(qual)}")
    print(f"  Correlation Raw VA vs Role-Adjusted VA: {qual['raw_va_per_ball'].corr(qual['role_adj_va_per_ball']):.4f}")
    print(f"  Mean Absolute Shift: {qual['va_shift'].abs().mean():.4f} runs/ball")
    print(f"  Max Positive Shift: {qual['va_shift'].max():+.4f} runs/ball")
    print(f"  Max Negative Shift: {qual['va_shift'].min():+.4f} runs/ball")


if __name__ == "__main__":
    main()
