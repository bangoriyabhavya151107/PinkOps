"""
PinkOps — Stage 4.0: Player Attribution Module (Remediated)
Module: src/stage_4_0/attribution.py

Purpose:
- Compute delivery-level and player-level Value Added (VA) above expectation.
- Strictly adhere to verified cricket attribution accounting:
  - Batter: Runs off bat strictly; exclude byes, leg-byes, wides, penalties.
  - Bowler: Runs conceded strictly; exclude byes, leg-byes, penalties; include wides and no-balls.
  - Dismissals: Isolate bowler-attributable wickets from run-outs, retire out, and retired hurt.
"""

import pandas as pd
import numpy as np


def compute_delivery_va(df: pd.DataFrame, exp_col: str = 'expected_runs') -> pd.DataFrame:
    """Computes delivery-level Value Added with strict actor-level attribution."""
    df_out = df.copy()
    expected = df_out[exp_col]
    
    # 1. Batter runs scored (strictly runs off bat)
    bat_runs = df_out['runs'].fillna(0).astype(int)
    
    # 2. Bowler runs conceded:
    # Exclude byes, legbyes, Penalty
    # Include bat runs + wides + noballs (Overstep, other)
    extras_type = df_out['extras_type'].fillna('None')
    extras_runs = (df_out['extras1_runs'].fillna(0) + df_out['extras_2_runs'].fillna(0)).astype(int)
    
    bowler_runs_conceded = bat_runs.copy()
    # Add extras for wide, Overstep, other
    bowler_extras_mask = extras_type.isin(['wide', 'Overstep', 'other'])
    bowler_runs_conceded = np.where(bowler_extras_mask, bat_runs + extras_runs, bat_runs)
    
    df_out['bat_runs_attributed'] = bat_runs
    df_out['bowler_runs_conceded'] = bowler_runs_conceded
    
    # Value Added calculations
    # Batter Value Added: actual runs off bat minus expected runs
    df_out['va_batter'] = bat_runs - expected
    
    # Bowler Value Added: expected runs conceded minus actual runs conceded
    df_out['va_bowler'] = expected - bowler_runs_conceded
    
    # Boundary definitions
    df_out['is_bat_boundary'] = (df_out['is_four'] | df_out['is_six']).astype(int)
    df_out['is_bowler_boundary'] = (
        (df_out['is_four'] | df_out['is_six']) | 
        (bowler_extras_mask & (df_out['runs_on_delivery'] >= 4))
    ).astype(int)
    
    # Dot ball definitions
    # Batter dot: 0 runs off bat on a non-wide
    df_out['is_bat_dot'] = ((bat_runs == 0) & (extras_type != 'wide')).astype(int)
    # Bowler dot: 0 runs conceded on a legal delivery (no wide, noball)
    df_out['is_bowler_dot'] = ((bowler_runs_conceded == 0) & (~bowler_extras_mask)).astype(int)
    
    # Single definition (strike rotation)
    df_out['is_single'] = (bat_runs == 1).astype(int)
    
    # Batter-attributable execution dismissal
    stroke_dismissals = ['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket']
    df_out['is_batter_dismissal'] = (
        (df_out['dismissed_player_id_cleaned'] == df_out['striker_id']) &
        (df_out['dismissal_type_cleaned'].isin(stroke_dismissals))
    ).astype(int)
    
    return df_out


def calculate_player_va(df_with_va: pd.DataFrame, role: str = 'batter') -> pd.DataFrame:
    """
    Aggregates player-level Value Added and multi-dimensional execution metrics.
    """
    player_col = 'striker_id' if role == 'batter' else 'bowler_id'
    va_col = 'va_batter' if role == 'batter' else 'va_bowler'
    runs_col = 'bat_runs_attributed' if role == 'batter' else 'bowler_runs_conceded'
    dot_col = 'is_bat_dot' if role == 'batter' else 'is_bowler_dot'
    boundary_col = 'is_bat_boundary' if role == 'batter' else 'is_bowler_boundary'
    wicket_col = 'is_batter_dismissal' if role == 'batter' else 'is_bowler_wicket'
    exp_col = 'expected_runs'
    
    records = []
    for p_id, g in df_with_va.groupby(player_col):
        # For batters, filter out wides from balls faced where appropriate, or retain for sample
        n = len(g)
        p_mask = g['is_high_pressure'] == 1
        p_balls = p_mask.sum()
        
        # Raw totals
        act_runs = g[runs_col].sum()
        exp_runs = g[exp_col].sum()
        raw_va = g[va_col].sum()
        raw_va_per_ball = raw_va / n if n > 0 else 0.0
        
        # Pressure-specific VA
        if p_balls > 0:
            pressure_va_per_ball = g.loc[p_mask, va_col].mean()
            pressure_act_runs = g.loc[p_mask, runs_col].mean()
            pressure_exp_runs = g.loc[p_mask, exp_col].mean()
        else:
            pressure_va_per_ball = 0.0
            pressure_act_runs = 0.0
            pressure_exp_runs = 0.0
            
        # Detailed components
        boundary_rate = g[boundary_col].mean()
        dot_rate = g[dot_col].mean()
        wicket_rate = g[wicket_col].mean()
        strike_rotation_rate = g['is_single'].mean()
        
        records.append({
            'player_id': p_id,
            'role': role,
            'total_deliveries': n,
            'pressure_deliveries': int(p_balls),
            'actual_performance_mean': round(float(act_runs / n), 4),
            'expected_performance_mean': round(float(exp_runs / n), 4),
            'raw_va_per_ball': round(float(raw_va_per_ball), 4),
            'pressure_va_per_ball': round(float(pressure_va_per_ball), 4),
            'boundary_execution_rate': round(float(boundary_rate), 4),
            'dot_execution_rate': round(float(dot_rate), 4),
            'wicket_execution_rate': round(float(wicket_rate), 4),
            'strike_rotation_rate': round(float(strike_rotation_rate), 4)
        })
        
    return pd.DataFrame(records)
