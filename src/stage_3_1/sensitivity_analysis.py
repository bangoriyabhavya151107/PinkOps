"""
PinkOps — Stage 3.1: Hyperparameter Sensitivity Engine
Module: src/stage_3_1/sensitivity_analysis.py

Purpose:
- Evaluate RDI epsilon sensitivity (0.05, 0.10, 0.15, 0.20, 0.30)
- Evaluate Venue shrinkage K sensitivity (100, 250, 500, 1000, 2000)
- Evaluate Opposition Elo K sensitivity (16, 32, 48)
- Evaluate Lower Credible Bound (LCB) percentile sensitivity (10th, 20th, 25th, 30th)
- Output data/processed/stage_3_1_pressure_sensitivity.csv
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path


def run_rdi_sensitivity(df: pd.DataFrame):
    """Profile RDI distributions and extreme values across epsilons."""
    epsilons = [0.05, 0.10, 0.15, 0.20, 0.30]
    records = []
    for eps in epsilons:
        rdi = df['wickets_before'] / (df['innings_progress_before'] + eps)
        # Count batters facing >= 30 balls under RDI >= 5.0
        bat_crisis = df.groupby('striker_id').apply(lambda g: (rdi.loc[g.index] >= 5.0).sum())
        qual_batters = (bat_crisis >= 30).sum()

        records.append({
            'experiment_type': 'RDI Epsilon',
            'parameter': f'eps={eps}',
            'mean': round(float(rdi.mean()), 3),
            'std': round(float(rdi.std()), 3),
            'median': round(float(rdi.median()), 3),
            'p75': round(float(rdi.quantile(0.75)), 3),
            'p95': round(float(rdi.quantile(0.95)), 3),
            'p99': round(float(rdi.quantile(0.99)), 3),
            'max': round(float(rdi.max()), 3),
            'corr_with_wickets': round(float(rdi.corr(df['wickets_before'])), 3),
            'corr_with_progress': round(float(rdi.corr(df['innings_progress_before'])), 3),
            'qualified_players_count': int(qual_batters),
            'stability_status': 'Optimal' if eps == 0.15 else ('Acceptable' if eps in [0.10, 0.20] else 'Extreme/Attenuated')
        })
    return pd.DataFrame(records)


def run_venue_sensitivity(df: pd.DataFrame):
    """Evaluate venue shrinkage K values."""
    global_mean = df['runs_on_delivery'].mean()
    venue_stats = df.groupby('venue_id')['runs_on_delivery'].agg(['count', 'mean']).reset_index()
    k_values = [100, 250, 500, 1000, 2000]
    records = []

    for K in k_values:
        shrunk = (venue_stats['count'] * venue_stats['mean'] + K * global_mean) / (venue_stats['count'] + K)
        diff = np.abs(shrunk - venue_stats['mean'])
        low_sample = venue_stats['count'] <= 250
        diff_low = diff[low_sample]

        records.append({
            'experiment_type': 'Venue Shrinkage K',
            'parameter': f'K={K}',
            'mean': round(float(shrunk.mean()), 3),
            'std': round(float(shrunk.std()), 3),
            'median': round(float(shrunk.median()), 3),
            'p75': round(float(shrunk.quantile(0.75)), 3),
            'p95': round(float(shrunk.quantile(0.95)), 3),
            'p99': round(float(shrunk.quantile(0.99)), 3),
            'max': round(float(shrunk.max()), 3),
            'corr_with_wickets': round(float(diff.mean()), 3), # average shrinkage overall
            'corr_with_progress': round(float(diff_low.mean()), 3), # average shrinkage low-sample
            'qualified_players_count': int(len(venue_stats)),
            'stability_status': 'Optimal' if K == 500 else ('Under-shrunk' if K < 500 else 'Over-shrunk')
        })
    return pd.DataFrame(records)


def run_elo_sensitivity(df_matches: pd.DataFrame):
    """Evaluate team Elo ratings across K=16, 32, 48."""
    k_values = [16, 32, 48]
    records = []

    for K in k_values:
        elo = {}
        for idx, row in df_matches.iterrows():
            t1, t2 = row['home_team_id'], row['away_team_id']
            r1 = elo.get(t1, 1500.0)
            r2 = elo.get(t2, 1500.0)
            exp1 = 1.0 / (1.0 + 10.0 ** ((r2 - r1) / 400.0))

            win_team = row['win_team_id']
            margin_type = row['post_margin_type']
            if pd.isna(win_team) or margin_type in ['none']:
                continue
            elif win_team == t1:
                s1, s2 = 1.0, 0.0
            elif win_team == t2:
                s1, s2 = 0.0, 1.0
            else:
                s1, s2 = 0.5, 0.5

            elo[t1] = r1 + K * (s1 - exp1)
            elo[t2] = r2 + K * (s2 - (1.0 - exp1))

        ratings = list(elo.values())
        records.append({
            'experiment_type': 'Elo Responsiveness K',
            'parameter': f'K={K}',
            'mean': round(float(np.mean(ratings)), 3),
            'std': round(float(np.std(ratings)), 3),
            'median': round(float(np.median(ratings)), 3),
            'p75': round(float(np.quantile(ratings, 0.75)), 3),
            'p95': round(float(np.quantile(ratings, 0.95)), 3),
            'p99': round(float(np.quantile(ratings, 0.99)), 3),
            'max': round(float(np.max(ratings)), 3),
            'corr_with_wickets': round(float(np.min(ratings)), 3), # min rating
            'corr_with_progress': round(float(np.max(ratings) - np.min(ratings)), 3), # rating spread
            'qualified_players_count': int(len(elo)),
            'stability_status': 'Optimal' if K == 32 else ('Sluggish' if K == 16 else 'Volatile')
        })
    return pd.DataFrame(records)


def run_lcb_sensitivity():
    """Evaluate LCB percentiles (10th, 20th, 25th, 30th) on player opportunity data."""
    opp_path = Path("D:/PinkOps/data/processed/player_opportunity_profiles.parquet")
    df_opp = pd.read_parquet(opp_path)
    batters = df_opp[df_opp['role'] == 'batter'].copy()

    SIGMA = 1.6
    K_SHRINK = 100.0
    batters['raw_rate'] = (batters['total_runs'] / batters['total_balls']) - 1.41
    batters['shrunk_mean'] = (batters['total_balls'] * batters['raw_rate']) / (batters['total_balls'] + K_SHRINK)
    batters['se'] = SIGMA / np.sqrt(batters['total_balls'] + K_SHRINK)

    lcb_specs = [
        ('10th Percentile', 1.282),
        ('20th Percentile', 0.842),
        ('25th Percentile', 0.674),
        ('30th Percentile', 0.524)
    ]
    records = []
    top_sm = set(batters.nlargest(20, 'shrunk_mean')['player_id'])

    for name, z in lcb_specs:
        lcb = batters['shrunk_mean'] - z * batters['se']
        rank_corr = batters['shrunk_mean'].corr(lcb, method='spearman')
        top_lcb = set(batters.assign(score=lcb).nlargest(20, 'score')['player_id'])
        overlap = len(top_sm.intersection(top_lcb)) / 20.0

        records.append({
            'experiment_type': 'LCB Percentile',
            'parameter': name,
            'mean': round(float(lcb.mean()), 3),
            'std': round(float(lcb.std()), 3),
            'median': round(float(lcb.median()), 3),
            'p75': round(float(lcb.quantile(0.75)), 3),
            'p95': round(float(lcb.quantile(0.95)), 3),
            'p99': round(float(lcb.quantile(0.99)), 3),
            'max': round(float(lcb.max()), 3),
            'corr_with_wickets': round(float(rank_corr), 3), # spearman rank corr with posterior mean
            'corr_with_progress': round(float(overlap), 3), # top-20 overlap ratio
            'qualified_players_count': int(len(batters)),
            'stability_status': 'Optimal' if z == 0.842 else 'Sensitivity Test'
        })
    return pd.DataFrame(records)


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    out_csv = project_root / "data" / "processed" / "stage_3_1_pressure_sensitivity.csv"

    con = duckdb.connect()
    df = con.execute(f"""
        SELECT 
            match_id, innings, wickets_before, innings_progress_before,
            runs_on_delivery, venue_id, striker_id
        FROM '{parquet_path.as_posix()}'
    """).df()

    df_matches = con.execute(f"""
        SELECT DISTINCT
            match_id, match_date, home_team_id, away_team_id,
            win_team_id, post_margin_type
        FROM '{parquet_path.as_posix()}'
        ORDER BY match_date, match_id
    """).df()

    print("Executing Stage 3.1 Sensitivity Analysis across all four dimensions...")
    rdi_df = run_rdi_sensitivity(df)
    venue_df = run_venue_sensitivity(df)
    elo_df = run_elo_sensitivity(df_matches)
    lcb_df = run_lcb_sensitivity()

    all_sens = pd.concat([rdi_df, venue_df, elo_df, lcb_df], ignore_index=True)
    all_sens.to_csv(out_csv, index=False)
    print(f"Saved complete sensitivity results ({len(all_sens)} specifications) to {out_csv}")


if __name__ == "__main__":
    main()
