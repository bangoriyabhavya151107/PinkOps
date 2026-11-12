"""
PinkOps — Stage 3.1: First-Innings Scoring-Trajectory Hardening
Module: src/stage_3_1/pressure_trajectory.py

Purpose:
- Construct pre-delivery first-innings trajectory expectation: ExpectedCumulativeRuns(t)
- Derive TrajectoryDeficit(t) = ExpectedCumulativeRuns(t) - ActualCumulativeRunsBefore(t)
- Standardize TrajectoryDeficitZ(t) using robust empirical scale per over/progress state
- Strictly decouple Resource Pressure from Scoring-Trajectory Pressure
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score


def build_trajectory_models(df_inn1: pd.DataFrame):
    """
    Fit empirical pre-delivery scoring-trajectory expectation model on 1st innings.
    Accounts strictly for pre-delivery variables:
    - legal_balls_bowled, balls_sq
    - phase (Powerplay, Middle, Death)
    - venue baseline (shrunk)
    - competition baseline
    - team pre-match Elos
    """
    df = df_inn1.copy()
    df['balls'] = df['legal_balls_bowled']
    df['balls_sq'] = df['balls'] ** 2
    df['is_powerplay'] = (df['overid'] <= 5).astype(int)
    df['is_death'] = (df['overid'] >= 15).astype(int)

    # 1. Situational Par Trajectory (Innings progress, phase, venue, comp)
    bench_features = ['balls', 'balls_sq', 'is_powerplay', 'is_death', 'venue_baseline', 'comp_baseline']
    X_bench = df[bench_features].fillna(0)
    y = df['runs_before']

    model_bench = Ridge(alpha=100.0).fit(X_bench, y)
    df['expected_cum_runs_par'] = model_bench.predict(X_bench)
    df['trajectory_deficit_par'] = df['expected_cum_runs_par'] - df['runs_before']

    # 2. Context + Opponent Full State Trajectory (adds wickets in hand and Elo)
    full_features = bench_features + ['wickets_in_hand_before', 'home_pre_match_elo', 'away_pre_match_elo']
    X_full = df[full_features].fillna(0)
    model_full = Ridge(alpha=100.0).fit(X_full, y)
    df['expected_cum_runs_full'] = model_full.predict(X_full)
    df['trajectory_deficit_full'] = df['expected_cum_runs_full'] - df['runs_before']

    # Compute robust scale per over for standardization
    scale_by_over = df.groupby('overid')['runs_before'].agg(
        lambda s: (s.quantile(0.75) - s.quantile(0.25)) / 1.349
    ).to_dict()

    df['robust_scale'] = df['overid'].map(scale_by_over).fillna(15.0).clip(lower=4.0)
    df['trajectory_deficit_z'] = df['trajectory_deficit_par'] / df['robust_scale']

    metrics = {
        'par_r2': round(float(r2_score(y, df['expected_cum_runs_par'])), 4),
        'par_mae': round(float(mean_absolute_error(y, df['expected_cum_runs_par'])), 2),
        'full_r2': round(float(r2_score(y, df['expected_cum_runs_full'])), 4),
        'full_mae': round(float(mean_absolute_error(y, df['expected_cum_runs_full'])), 2)
    }

    return df, model_bench, model_full, metrics


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    venue_path = project_root / "data" / "processed" / "venue_baselines.csv"
    comp_path = project_root / "data" / "processed" / "competition_baselines.csv"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"

    con = duckdb.connect()
    query = f"""
    SELECT 
        m.match_id, m.innings, m.innings_ball_num, m.overid, m.legal_balls_bowled,
        m.scheduled_balls, m.innings_progress_before, m.wickets_before, m.wickets_in_hand_before,
        m.runs_before, m.season, m.comp_id, m.venue_id,
        v.shrunk_avg_runs_per_ball as venue_baseline,
        c.avg_runs_per_ball as comp_baseline,
        e.home_pre_match_elo, e.away_pre_match_elo
    FROM '{parquet_path.as_posix()}' m
    LEFT JOIN '{venue_path.as_posix()}' v ON m.venue_id = v.venue_id
    LEFT JOIN '{comp_path.as_posix()}' c ON m.comp_id = c.comp_id
    LEFT JOIN '{elo_path.as_posix()}' e ON m.match_id = e.match_id
    WHERE m.innings = 1
    """
    df_inn1 = con.execute(query).df()
    print(f"Loaded {len(df_inn1)} first-innings deliveries.")

    df_res, m_bench, m_full, metrics = build_trajectory_models(df_inn1)
    print(f"Par Trajectory Model:  R2 = {metrics['par_r2']}, MAE = {metrics['par_mae']} runs")
    print(f"Full Trajectory Model: R2 = {metrics['full_r2']}, MAE = {metrics['full_mae']} runs")

    # Audit the key motivating case: 25/3 at over 4 vs 55/3 at over 4
    # Over 4 = ~24 legal balls bowled, venue = 1.41, comp = 1.41
    sample_bench_24 = m_bench.predict([[24, 576, 1, 0, 1.41, 1.41]])[0]
    print(f"\nAudit Case: Over 4 (24 balls) Par Expected Runs = {sample_bench_24:.1f}")
    print(f"  Team A at 25/3: Deficit = {sample_bench_24 - 25:+.1f} runs (Behind par, Dual Pressure: Crisis + Trajectory Deficit)")
    print(f"  Team B at 55/3: Deficit = {sample_bench_24 - 55:+.1f} runs (Surplus of {55 - sample_bench_24:.1f} runs! Resource Pressure only, Trajectory Healthy)")


if __name__ == "__main__":
    main()
