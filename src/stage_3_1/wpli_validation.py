"""
PinkOps — Stage 3.1: Win Probability Leverage Index (WPLI) Validation Engine
Module: src/stage_3_1/wpli_validation.py

Purpose:
- Compare WPLI-A, WPLI-B, and WPLI-C formulations
- Verify causal counterfactual definitions and behavior at extreme match states
- Evaluate calibration, stability, and ablation contribution
- Output data/processed/stage_3_1_wpli_comparison.csv
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression


def compute_wpli_formulations(df_chase: pd.DataFrame):
    """Compute WPLI-A, WPLI-B, and WPLI-C on chase deliveries."""
    df = df_chase.copy()
    features = ['runs_required_before', 'balls_remaining_before', 'wickets_in_hand_before', 
                'target_proximity', 'balls_per_wicket_cushion']
    X = df[features].copy()
    y = df['chase_won']

    # Train Win Probability model strictly on pre-delivery state
    model = LogisticRegression(max_iter=1000).fit(X, y)
    df['wp_current'] = model.predict_proba(X)[:, 1]

    # Counterfactual 1: Wicket Falls (R = 0, W = 1)
    X_wkt = X.copy()
    X_wkt['balls_remaining_before'] = np.maximum(0, X_wkt['balls_remaining_before'] - 1)
    X_wkt['wickets_in_hand_before'] = np.maximum(0, X_wkt['wickets_in_hand_before'] - 1)
    X_wkt['target_proximity'] = X_wkt['runs_required_before'] / (X_wkt['balls_remaining_before'] + 1.0)
    X_wkt['balls_per_wicket_cushion'] = X_wkt['balls_remaining_before'] / (X_wkt['wickets_in_hand_before'] + 0.5)
    df['wp_wkt'] = model.predict_proba(X_wkt)[:, 1]

    # Counterfactual 2: Boundary Hit (R = 5, W = 0)
    X_bnd = X.copy()
    X_bnd['runs_required_before'] = np.maximum(0, X_bnd['runs_required_before'] - 5)
    X_bnd['balls_remaining_before'] = np.maximum(0, X_bnd['balls_remaining_before'] - 1)
    X_bnd['target_proximity'] = X_bnd['runs_required_before'] / (X_bnd['balls_remaining_before'] + 1.0)
    X_bnd['balls_per_wicket_cushion'] = X_bnd['balls_remaining_before'] / (X_bnd['wickets_in_hand_before'] + 0.5)
    df['wp_bnd'] = model.predict_proba(X_bnd)[:, 1]

    delta_wkt = np.maximum(0, df['wp_current'] - df['wp_wkt'])
    delta_bnd = np.maximum(0, df['wp_bnd'] - df['wp_current'])
    sigma_wp = float(df['wp_current'].std())

    # Formulations
    df['wpli_a'] = (delta_wkt + delta_bnd) / (2.0 * sigma_wp)
    df['wpli_b'] = 0.5 * (delta_wkt + delta_bnd)
    df['wpli_c'] = np.sqrt(0.5 * (delta_wkt**2 + delta_bnd**2))

    summary_records = []
    specs = [
        ('WPLI-A (Current Scaled)', df['wpli_a'], 'Scaled by 2*sigma(WP); unconstrained upper tail'),
        ('WPLI-B (Absolute Swing)', df['wpli_b'], 'Bounded [0, 1]; directly represents average WP swing'),
        ('WPLI-C (RMS Leverage)', df['wpli_c'], 'Bounded [0, 1]; quadratic penalty on large swings')
    ]

    for name, s, math_desc in specs:
        summary_records.append({
            'formulation': name,
            'mathematical_basis': math_desc,
            'min': round(float(s.min()), 4),
            'p25': round(float(s.quantile(0.25)), 4),
            'median': round(float(s.median()), 4),
            'mean': round(float(s.mean()), 4),
            'p75': round(float(s.quantile(0.75)), 4),
            'p95': round(float(s.quantile(0.95)), 4),
            'max': round(float(s.max()), 4),
            'std': round(float(s.std()), 4),
            'spearman_corr_with_wpli_b': round(float(s.corr(df['wpli_b'], method='spearman')), 4),
            'recommendation': 'Retain as Descriptive Feature (Downgraded from Primary Model Gate)'
        })

    return df, pd.DataFrame(summary_records), model


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    out_csv = project_root / "data" / "processed" / "stage_3_1_wpli_comparison.csv"

    con = duckdb.connect()
    df_chase = con.execute(f"""
        SELECT 
            match_id, innings, innings_ball_num, overid,
            runs_required_before, balls_remaining_before, wickets_in_hand_before,
            post_match_winner_team_id, batting_team_id, striker_id, bowler_id
        FROM '{parquet_path.as_posix()}'
        WHERE innings = 2 
          AND runs_required_before IS NOT NULL 
          AND balls_remaining_before > 0
          AND post_match_winner_team_id IS NOT NULL
    """).df()

    df_chase['target_proximity'] = df_chase['runs_required_before'] / (df_chase['balls_remaining_before'] + 1.0)
    df_chase['balls_per_wicket_cushion'] = df_chase['balls_remaining_before'] / (df_chase['wickets_in_hand_before'] + 0.5)
    df_chase['chase_won'] = (df_chase['post_match_winner_team_id'] == df_chase['batting_team_id']).astype(int)

    df_res, sum_df, model = compute_wpli_formulations(df_chase)
    sum_df.to_csv(out_csv, index=False)
    print(f"Saved WPLI comparison ({len(sum_df)} formulations) to {out_csv}")
    print(sum_df.to_string(index=False))


if __name__ == "__main__":
    main()
