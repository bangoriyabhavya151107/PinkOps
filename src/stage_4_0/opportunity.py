"""
PinkOps — Stage 4.0: Pressure Opportunity Module
Module: src/stage_4_0/opportunity.py

Purpose:
- Rigorously separate Pressure Opportunity from Player Execution.
- Compute continuous delivery-level pressure intensity P(t^-) in [0, 1].
- Distinguish raw exposure, weighted exposure, and evidence tiers.
"""

import pandas as pd
import numpy as np


def compute_delivery_pressure_intensity(df: pd.DataFrame, epsilon: float = 0.15) -> pd.Series:
    """
    Computes continuous delivery-level pressure intensity P(t^-) in [0, 1].
    
    Dimensions:
    1. Resource Scarcity: RDI = wickets_before / (innings_progress_before + epsilon)
       Normalized by baseline crisis threshold (RDI / 8.0 clipped to [0, 1])
    2. Rate Stress / Temporal Urgency:
       - In chases: Target proximity = runs_required / (balls_rem + 1.0)
         Normalized against baseline 1.5 runs/ball: min(1.0, max(0.0, (target_prox - 1.0) / 1.5))
       - In 1st innings: Death phase indicator and Trajectory Deficit
         min(1.0, max(0.0, traj_deficit / 25.0))
    3. Cushion Deficit:
       Balls per wicket cushion < 6 balls/wicket implies elevated pressure
    """
    # 1. Resource scarcity component
    rdi = df['wickets_before'] / (df['innings_progress_before'] + epsilon)
    rdi_comp = np.clip(rdi / 8.0, 0.0, 1.0)

    # 2. Rate / Trajectory urgency component
    # Chase rate urgency
    chase_mask = df['is_chase'].astype(bool)
    chase_urgency = np.zeros(len(df))
    if 'target_proximity' in df.columns:
        prox = df['target_proximity'].fillna(0.0)
    else:
        prox = df['runs_required_before'].fillna(0.0) / (df['balls_remaining_before'] + 1.0)
    chase_urgency[chase_mask] = np.clip((prox[chase_mask] - 1.0) / 1.5, 0.0, 1.0)

    # 1st innings trajectory deficit urgency
    inn1_mask = ~chase_mask
    inn1_urgency = np.zeros(len(df))
    if 'trajectory_deficit' in df.columns:
        t_def = df['trajectory_deficit'].fillna(0.0)
        inn1_urgency[inn1_mask] = np.clip(t_def[inn1_mask] / 25.0, 0.0, 1.0)
    
    # Phase urgency (death overs naturally elevate urgency)
    is_death = (df['overid'] >= 15).astype(float)
    urgency_comp = np.where(chase_mask, chase_urgency, np.maximum(inn1_urgency, 0.5 * is_death))

    # 3. Continuous composite pressure intensity P(t^-) in [0, 1]
    # Equal contribution of resource scarcity and rate/trajectory urgency
    pressure_intensity = 0.5 * rdi_comp + 0.5 * urgency_comp
    return pressure_intensity.clip(0.0, 1.0)


def build_pressure_opportunity(df: pd.DataFrame, epsilon: float = 0.15) -> pd.DataFrame:
    """
    Enriches delivery dataframe with:
    - pressure_intensity: continuous P(t^-) in [0, 1]
    - is_high_pressure: flag for P(t^-) >= 0.50
    """
    df_out = df.copy()
    df_out['pressure_intensity'] = compute_delivery_pressure_intensity(df_out, epsilon=epsilon)
    df_out['is_high_pressure'] = (df_out['pressure_intensity'] >= 0.50).astype(int)
    return df_out


def aggregate_player_exposure(df_with_opp: pd.DataFrame, role: str = 'batter') -> pd.DataFrame:
    """
    Aggregates player-level exposure metrics:
    - total_opportunities (raw delivery count)
    - pressure_opportunities (count where is_high_pressure == 1)
    - weighted_pressure_exposure (sum of continuous pressure intensity)
    - pressure_exposure_pct (weighted exposure / total balls)
    - evidence_tier ('Robust Evidence', 'Moderate Evidence', 'Sparse Evidence')
    """
    player_col = 'striker_id' if role == 'batter' else 'bowler_id'
    
    agg = df_with_opp.groupby(player_col).agg(
        total_opportunities=('runs_on_delivery', 'count'),
        pressure_opportunities=('is_high_pressure', 'sum'),
        weighted_pressure_exposure=('pressure_intensity', 'sum'),
        mean_pressure_intensity=('pressure_intensity', 'mean'),
        matches_played=('match_id', 'nunique')
    ).reset_index().rename(columns={player_col: 'player_id'})

    agg['role'] = role
    agg['pressure_exposure_pct'] = (agg['weighted_pressure_exposure'] / agg['total_opportunities'] * 100.0).round(2)

    def classify_tier(row):
        # Governance tiers:
        # Robust Evidence: >= 150 total balls and >= 40 pressure balls
        # Moderate Evidence: >= 50 total balls and >= 15 pressure balls
        # Sparse Evidence: otherwise
        if row['total_opportunities'] >= 150 and row['pressure_opportunities'] >= 40:
            return 'Robust Evidence'
        elif row['total_opportunities'] >= 50 and row['pressure_opportunities'] >= 15:
            return 'Moderate Evidence'
        else:
            return 'Sparse Evidence'

    agg['evidence_tier'] = agg.apply(classify_tier, axis=1)
    return agg
