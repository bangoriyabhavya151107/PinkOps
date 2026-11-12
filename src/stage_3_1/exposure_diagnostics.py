"""
PinkOps — Stage 3.1: Participation & Exposure-Bias Diagnostics Engine
Module: src/stage_3_1/exposure_diagnostics.py

Purpose:
- Profile delivery-level exposure across all 888 batters and 647 bowlers
- Quantify high-pressure exposure percentage, phase breakdown, and median intensity
- Identify low-exposure players and flag small-sample uncertainty
- Output data/processed/stage_3_1_player_exposure.csv
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path


def calculate_exposure_diagnostics(df: pd.DataFrame):
    """Compute detailed exposure profiles for every batter and bowler."""
    # Define high pressure delivery criteria:
    # 1. Chases with RRR >= 10.0 OR
    # 2. 1st innings Death Overs (15-19) OR
    # 3. 1st innings acute crisis (RDI >= 5.0)
    df['is_high_pressure'] = (
        ((df['innings'] == 2) & (df['required_run_rate_before'] >= 10.0)) |
        ((df['innings'] == 1) & (df['overid'] >= 15)) |
        ((df['innings'] == 1) & (df['resource_depletion_index'] >= 5.0))
    )

    # Batters
    bat_exp = df.groupby('striker_id').agg(
        total_matches=('match_id', 'nunique'),
        total_deliveries=('runs_on_delivery', 'count'),
        total_runs=('runs', 'sum'),
        dismissals=('is_wicket', lambda x: ((x) & (df.loc[x.index, 'dismissed_player_id_cleaned'] == df.loc[x.index, 'striker_id'])).sum()),
        pressure_matches=('match_id', lambda x: df.loc[x.index[df.loc[x.index, 'is_high_pressure']], 'match_id'].nunique()),
        pressure_deliveries=('is_high_pressure', 'sum'),
        powerplay_balls=('overid', lambda x: (x <= 5).sum()),
        middle_balls=('overid', lambda x: ((x >= 6) & (x <= 14)).sum()),
        death_balls=('overid', lambda x: (x >= 15).sum()),
        median_rdi=('resource_depletion_index', 'median')
    ).reset_index().rename(columns={'striker_id': 'player_id'})
    bat_exp['role'] = 'batter'

    # Bowlers
    bowl_exp = df.groupby('bowler_id').agg(
        total_matches=('match_id', 'nunique'),
        total_deliveries=('runs_on_delivery', 'count'),
        total_runs=('runs_on_delivery', 'sum'),
        dismissals=('is_bowler_wicket', 'sum'),
        pressure_matches=('match_id', lambda x: df.loc[x.index[df.loc[x.index, 'is_high_pressure']], 'match_id'].nunique()),
        pressure_deliveries=('is_high_pressure', 'sum'),
        powerplay_balls=('overid', lambda x: (x <= 5).sum()),
        middle_balls=('overid', lambda x: ((x >= 6) & (x <= 14)).sum()),
        death_balls=('overid', lambda x: (x >= 15).sum()),
        median_rdi=('resource_depletion_index', 'median')
    ).reset_index().rename(columns={'bowler_id': 'player_id'})
    bowl_exp['role'] = 'bowler'

    combined = pd.concat([bat_exp, bowl_exp], ignore_index=True)
    combined['pressure_exposure_pct'] = (combined['pressure_deliveries'] / combined['total_deliveries'] * 100.0).round(2)
    
    # Evidence categorization
    # Robust: >= 150 balls & >= 40 pressure balls
    # Moderate: >= 50 balls & >= 15 pressure balls
    # Low / Sparse: < 50 balls or < 15 pressure balls
    def get_evidence_tier(row):
        if row['total_deliveries'] >= 150 and row['pressure_deliveries'] >= 40:
            return 'Robust Evidence'
        elif row['total_deliveries'] >= 50 and row['pressure_deliveries'] >= 15:
            return 'Moderate Evidence'
        else:
            return 'Low / Sparse Evidence'

    combined['evidence_tier'] = combined.apply(get_evidence_tier, axis=1)
    combined['is_low_exposure'] = (combined['evidence_tier'] == 'Low / Sparse Evidence').astype(int)

    return combined


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    out_csv = project_root / "data" / "processed" / "stage_3_1_player_exposure.csv"

    con = duckdb.connect()
    query = f"""
    SELECT 
        match_id, innings, innings_ball_num, overid,
        striker_id, bowler_id, runs, runs_on_delivery, is_wicket,
        dismissed_player_id_cleaned, is_bowler_wicket,
        required_run_rate_before,
        (wickets_before * 1.0) / (innings_progress_before + 0.15) as resource_depletion_index
    FROM '{parquet_path.as_posix()}'
    WHERE innings IN (1, 2)
    """
    df = con.execute(query).df()
    print(f"Loaded {len(df)} deliveries for exposure diagnostics.")

    exp_df = calculate_exposure_diagnostics(df)
    exp_df.to_csv(out_csv, index=False)
    print(f"Saved exposure diagnostics for {len(exp_df)} player-roles to {out_csv}")

    print("\n--- Evidence Tier Summary ---")
    print(exp_df.groupby(['role', 'evidence_tier'])['player_id'].count().unstack())


if __name__ == "__main__":
    main()
