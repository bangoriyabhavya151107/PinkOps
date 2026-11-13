"""
PinkOps — Stage 4.0: Match Consistency Module
Module: src/stage_4_0/consistency.py

Purpose:
- Evaluate match-to-match performance stability across appearances.
- Compute Median Absolute Deviation (MAD), Interquartile Range (IQR), and tail risk.
- Ensure that players with high variance and isolated flukes are not mistaken for reliable performers.
"""

import pandas as pd
import numpy as np


def calculate_consistency(df_deliveries: pd.DataFrame, role: str = 'batter') -> pd.DataFrame:
    """
    Computes match-level stability and dispersion metrics for players.
    """
    player_col = 'striker_id' if role == 'batter' else 'bowler_id'
    va_col = 'va_batter' if role == 'batter' else 'va_bowler'
    
    # Aggregate Value Added at the match level
    match_agg = df_deliveries.groupby([player_col, 'match_id']).agg(
        match_balls=('runs_on_delivery', 'count'),
        match_va=(va_col, 'sum'),
        match_mean_va=(va_col, 'mean')
    ).reset_index()
    
    records = []
    for p_id, g in match_agg.groupby(player_col):
        n_matches = len(g)
        va_series = g['match_mean_va']
        
        # Dispersion metrics
        median_va = va_series.median()
        mad = np.median(np.abs(va_series - median_va))
        q75 = va_series.quantile(0.75)
        q25 = va_series.quantile(0.25)
        iqr = q75 - q25
        std_va = va_series.std() if n_matches > 1 else 0.0
        
        # Tail metrics
        neg_matches = (va_series < 0).sum()
        neg_match_pct = (neg_matches / n_matches * 100.0) if n_matches > 0 else 0.0
        p10_floor = va_series.quantile(0.10) if n_matches >= 5 else va_series.min()
        
        records.append({
            'player_id': p_id,
            'role': role,
            'matches_count': n_matches,
            'consistency_mad': round(float(mad), 4),
            'consistency_iqr': round(float(iqr), 4),
            'consistency_std': round(float(std_va), 4),
            'negative_match_pct': round(float(neg_match_pct), 2),
            'floor_va_p10': round(float(p10_floor), 4),
            'stability_index': round(float(1.0 / (1.0 + mad)), 4)
        })
        
    return pd.DataFrame(records)
