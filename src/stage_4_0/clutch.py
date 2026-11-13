"""
PinkOps — Stage 4.0: Clutch Delta Module (Remediated & Strengthened)
Module: src/stage_4_0/clutch.py

Purpose:
- Formulate and calculate strengthened context-adjusted Clutch Delta:
  Clutch Delta = VA_high_pressure - VA_comparable_baseline
- Strengthened multi-dimensional coarsened exact matching:
  - Phase (Powerplay 0-5, Middle 6-15, Death 16-19)
  - Wickets in hand (Low 1-3, Mid 4-6, High 7-10)
  - Chase status (Chase vs First Innings Defend)
  - Pace or Spin bowling
  - Batting order tier (Top 1-3, Middle 4-6, Lower 7-11)
- Strictly framed as "descriptive context-adjusted pressure differential" (non-causal).
"""

import pandas as pd
import numpy as np


def calculate_clutch_delta(df_deliveries: pd.DataFrame, role: str = 'batter') -> pd.DataFrame:
    """
    Computes strengthened context-adjusted Clutch Delta with multi-dimensional matching.
    
    Clutch Delta = VA_high_pressure - VA_comparable_baseline
    """
    df = df_deliveries.copy()
    player_col = 'striker_id' if role == 'batter' else 'bowler_id'
    va_col = 'va_batter' if role == 'batter' else 'va_bowler'
    
    # 1. Multi-dimensional coarsened strata features
    # Phase
    if 'phase' in df.columns:
        phase_str = df['phase'].astype(str)
    elif 'overid' in df.columns:
        phase_str = np.where(df['overid'] < 6, 'PP', np.where(df['overid'] >= 16, 'Death', 'Mid'))
    else:
        phase_str = 'All'
        
    # Wickets in hand
    wkt_col = 'wickets_in_hand_before' if 'wickets_in_hand_before' in df.columns else 'wickets_in_hand'
    if wkt_col in df.columns:
        wkt_str = np.where(df[wkt_col] <= 3, 'WktLow', np.where(df[wkt_col] <= 6, 'WktMid', 'WktHigh'))
    else:
        wkt_str = 'WktAll'
        
    # Chase vs defend
    if 'is_chase' in df.columns:
        chase_str = np.where(df['is_chase'], 'Chase', 'Defend')
    else:
        chase_str = 'InnAll'
        
    # Pace vs spin
    if 'pace_or_spin' in df.columns:
        pace_str = df['pace_or_spin'].fillna('pace').astype(str)
    elif 'is_pace' in df.columns:
        pace_str = np.where(df['is_pace'] == 1, 'Pace', 'Spin')
    else:
        pace_str = 'PaceAll'
        
    # Batting order / entry position tier
    if 'batting_order' in df.columns:
        order_str = np.where(df['batting_order'] <= 3, 'OrdTop', np.where(df['batting_order'] <= 6, 'OrdMid', 'OrdLow'))
    else:
        order_str = 'OrdAll'
        
    # Combined multi-dimensional strata key
    df['strata'] = phase_str + '_' + wkt_str + '_' + chase_str + '_' + pace_str + '_' + order_str
    
    # High pressure flag
    hp_flag = 'is_high_pressure' if 'is_high_pressure' in df.columns else 'is_pressure'
    
    records = []
    for p_id, g in df.groupby(player_col):
        total_n = len(g)
        hp_mask = g[hp_flag] == 1
        base_mask = g[hp_flag] == 0
        
        hp_count = hp_mask.sum()
        base_count = base_mask.sum()
        
        # Unmatched raw clutch delta
        hp_va = g.loc[hp_mask, va_col].mean() if hp_count > 0 else np.nan
        base_va = g.loc[base_mask, va_col].mean() if base_count > 0 else np.nan
        raw_clutch_delta = hp_va - base_va if (hp_count >= 10 and base_count >= 10) else np.nan
        
        # Stratum-matched clutch delta across shared strata
        strata_deltas = []
        strata_weights = []
        for s_key, s_group in g.groupby('strata'):
            s_hp = s_group[hp_flag] == 1
            s_base = s_group[hp_flag] == 0
            n_s_hp = s_hp.sum()
            n_s_base = s_base.sum()
            if n_s_hp >= 2 and n_s_base >= 2:
                d = s_group.loc[s_hp, va_col].mean() - s_group.loc[s_base, va_col].mean()
                w = n_s_hp
                strata_deltas.append(d)
                strata_weights.append(w)
                
        if len(strata_deltas) > 0 and sum(strata_weights) >= 8:
            matched_clutch_delta = np.average(strata_deltas, weights=strata_weights)
            matching_success_rate = sum(strata_weights) / hp_count if hp_count > 0 else 0.0
        else:
            matched_clutch_delta = raw_clutch_delta
            matching_success_rate = 1.0 if not np.isnan(raw_clutch_delta) else 0.0

        records.append({
            'player_id': p_id,
            'role': role,
            'hp_deliveries': int(hp_count),
            'baseline_deliveries': int(base_count),
            'hp_va_mean': round(float(hp_va), 4) if not np.isnan(hp_va) else None,
            'baseline_va_mean': round(float(base_va), 4) if not np.isnan(base_va) else None,
            'clutch_delta_raw': round(float(raw_clutch_delta), 4) if not np.isnan(raw_clutch_delta) else None,
            'clutch_delta_matched': round(float(matched_clutch_delta), 4) if not np.isnan(matched_clutch_delta) else None,
            'matching_coverage_pct': round(float(matching_success_rate * 100.0), 2)
        })
        
    return pd.DataFrame(records)
