"""
PinkOps — Stage 3.1: Expectation Estimand Definition & Modeling Engine
Module: src/stage_3_1/expectation_estimand.py

Purpose:
- Define and contrast:
  A. Situation-Only Contextual Expectation
  B. Context + Opponent-Quality Population Expectation
- Evaluate out-of-fold fit, MAE, RMSE, and feature contributions
- Provide precise statistical language: "contextual population expectation"
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold


def fit_expectation_estimands(df: pd.DataFrame):
    """Fit and contrast Estimand A (Situation-only) vs Estimand B (Context + Opponent)."""
    # Estimand A: Situation-Only
    feat_sit = [
        'innings_progress_before', 'wickets_in_hand_before', 'wickets_before',
        'is_powerplay', 'is_death', 'is_chase', 'venue_baseline', 'comp_baseline'
    ]
    # Estimand B: Context + Opponent Attack Quality
    feat_opp = feat_sit + [
        'home_pre_match_elo', 'away_pre_match_elo', 'is_pace',
        'recent_runs_12', 'recent_wickets_12', 'recent_dots_12'
    ]

    y = df['runs_on_delivery']
    groups = df['match_id']
    gkf = GroupKFold(n_splits=5)

    def evaluate_model(features, name):
        X = df[features].fillna(0)
        maes, rmses, r2s = [], [], []
        for train_idx, test_idx in gkf.split(X, y, groups):
            m = Ridge(alpha=100.0).fit(X.iloc[train_idx], y.iloc[train_idx])
            preds = m.predict(X.iloc[test_idx])
            maes.append(mean_absolute_error(y.iloc[test_idx], preds))
            rmses.append(np.sqrt(mean_squared_error(y.iloc[test_idx], preds)))
            r2s.append(r2_score(y.iloc[test_idx], preds))
        return {
            'estimand_name': name,
            'features_count': len(features),
            'cv_mae': round(float(np.mean(maes)), 4),
            'cv_mae_std': round(float(np.std(maes)), 4),
            'cv_rmse': round(float(np.mean(rmses)), 4),
            'cv_rmse_std': round(float(np.std(rmses)), 4),
            'cv_r2': round(float(np.mean(r2s)), 4),
            'interpretation': 'Situation-only environmental baseline' if 'Situation' in name else 'Contextual population expectation (Recommended for Player Attribution)'
        }

    res_sit = evaluate_model(feat_sit, 'Estimand A: Situation-Only Expectation')
    res_opp = evaluate_model(feat_opp, 'Estimand B: Context + Opponent Population Expectation')

    return pd.DataFrame([res_sit, res_opp])


def main():
    project_root = Path("D:/PinkOps")
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    venue_path = project_root / "data" / "processed" / "venue_baselines.csv"
    comp_path = project_root / "data" / "processed" / "competition_baselines.csv"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"

    con = duckdb.connect()
    query = f"""
    WITH base AS (
        SELECT 
            m.match_id, m.innings, m.innings_ball_num, m.overid,
            m.runs_on_delivery, m.is_legal_delivery, m.is_four, m.is_six, m.is_wicket,
            m.runs_before, m.wickets_before, m.wickets_in_hand_before,
            m.innings_progress_before, m.is_chase, m.pace_or_spin,
            v.shrunk_avg_runs_per_ball as venue_baseline,
            c.avg_runs_per_ball as comp_baseline,
            e.home_pre_match_elo, e.away_pre_match_elo,
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
        CASE WHEN overid <= 5 THEN 1 ELSE 0 END as is_powerplay,
        CASE WHEN overid >= 15 THEN 1 ELSE 0 END as is_death,
        CASE WHEN pace_or_spin = 'pace' THEN 1 ELSE 0 END as is_pace
    FROM base
    """
    df = con.execute(query).df()
    print(f"Loaded {len(df)} deliveries across 1st and 2nd innings.")

    estimand_df = fit_expectation_estimands(df)
    print("\n--- Expectation Estimands Comparison ---")
    print(estimand_df.to_string(index=False))


if __name__ == "__main__":
    main()
