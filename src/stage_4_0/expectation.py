"""
PinkOps — Stage 4.0: Contextual Expectation Module
Module: src/stage_4_0/expectation.py

Purpose:
- Build frozen contextual population expectation models for player attribution.
- Support both:
  - Specification B (Primary Frozen Estimand: Excludes recent 12-ball features to prevent endogenous self-absorption).
  - Specification A (Robustness Grid Estimand: Includes recent 12-ball micro-momentum).
- Controls for role confounding (batting order, balls consumed, bowling phase) and opponent quality.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge


def get_feature_list(spec: str = 'B', role_adjusted: bool = True) -> list:
    """Returns feature list for specified expectation model."""
    base_features = [
        'innings_progress_before', 'wickets_in_hand_before', 'wickets_before',
        'is_chase', 'is_powerplay', 'is_death', 'is_pace',
        'venue_baseline', 'comp_baseline',
        'home_pre_match_elo', 'away_pre_match_elo'
    ]
    
    if role_adjusted:
        base_features += ['batting_order', 'batter_balls_faced_before']
        
    if spec == 'A':
        base_features += ['recent_runs_12', 'recent_wickets_12', 'recent_dots_12']
        
    return base_features


def build_contextual_expectation(
    df: pd.DataFrame, 
    spec: str = 'B', 
    role_adjusted: bool = True,
    alpha: float = 100.0
) -> tuple[pd.Series, Ridge, list]:
    """
    Fits and generates delivery-level expected runs: E[Y(t) | X(t^-)].
    
    Parameters:
    - df: delivery-level DataFrame
    - spec: 'B' (Frozen Primary Estimand: pure exogenous context) or 'A' (includes recent 12 balls)
    - role_adjusted: whether to include batting order and balls already faced
    - alpha: L2 regularization strength
    
    Returns:
    - expected_runs: pd.Series of expected runs for each delivery
    - model: fitted Ridge regression model
    - features: list of features used
    """
    df_work = df.copy()
    if 'batting_order' not in df_work.columns:
        df_work['batting_order'] = 5.0
    else:
        df_work['batting_order'] = df_work['batting_order'].fillna(5.0)

    if 'batter_balls_faced_before' not in df_work.columns:
        df_work['batter_balls_faced_before'] = df_work.groupby(['match_id', 'innings', 'striker_id']).cumcount()

    features = get_feature_list(spec=spec, role_adjusted=role_adjusted)
    X = df_work[features].fillna(0.0)
    y = df_work['runs_on_delivery']

    model = Ridge(alpha=alpha).fit(X, y)
    expected_runs = pd.Series(model.predict(X), index=df.index, name=f'exp_runs_{spec}')
    return expected_runs, model, features
