"""
PinkOps — Stage 4.0: Downside Risk & Protection Module
Module: src/stage_4_0/downside.py

Purpose:
- Evaluate downside risk and failure rates under pressure.
- For Batters: Early dismissals (<= 5 balls), pressure collapse rate.
- For Bowlers: Blowout overs (15+ runs), boundary burst overs.
- Distinguish high average performance from robust downside protection.
"""

import pandas as pd
import numpy as np


def calculate_downside_metrics(df_deliveries: pd.DataFrame, role: str = 'batter') -> pd.DataFrame:
    """Computes context-adjusted downside risk metrics for players."""
    df = df_deliveries.copy()
    
    if role == 'batter':
        # Batter balls faced sequence within innings
        df['batter_ball_num'] = df.groupby(['match_id', 'innings', 'striker_id']).cumcount() + 1
        
        # Early dismissal: out within first 5 balls of innings
        df['is_early_dismissal'] = (
            (df['is_wicket']) & 
            (df['dismissed_player_id_cleaned'] == df['striker_id']) & 
            (df['batter_ball_num'] <= 5)
        ).astype(int)
        
        # Pressure duck / single digit: dismissed for <= 5 runs in innings
        inn_runs = df.groupby(['match_id', 'innings', 'striker_id']).agg(
            total_runs=('runs', 'sum'),
            was_out=('is_wicket', lambda s: (s & (df.loc[s.index, 'dismissed_player_id_cleaned'] == df.loc[s.index, 'striker_id'])).any()),
            had_pressure=('is_high_pressure', lambda s: s.any())
        ).reset_index()
        
        inn_runs['is_pressure_collapse'] = (
            (inn_runs['was_out']) & 
            (inn_runs['total_runs'] <= 5) & 
            (inn_runs['had_pressure'])
        ).astype(int)
        
        collapse_dict = inn_runs.groupby('striker_id')['is_pressure_collapse'].mean().to_dict()
        
        # Aggregate by player
        records = []
        for p_id, g in df.groupby('striker_id'):
            innings_count = g[['match_id', 'innings']].drop_duplicates().shape[0]
            early_outs = g['is_early_dismissal'].sum()
            early_out_rate = early_outs / innings_count if innings_count > 0 else 0.0
            collapse_rate = collapse_dict.get(p_id, 0.0)
            
            # Severe negative VA balls: high pressure dot ball or dismissal
            p_mask = g['is_high_pressure'] == 1
            if p_mask.sum() > 0:
                severe_neg = (g.loc[p_mask, 'runs_on_delivery'] == 0) | (g.loc[p_mask, 'is_wicket'])
                severe_neg_rate = severe_neg.mean()
            else:
                severe_neg_rate = 0.0
                
            records.append({
                'player_id': p_id,
                'role': 'batter',
                'early_dismissal_rate': round(float(early_out_rate), 4),
                'pressure_collapse_rate': round(float(collapse_rate), 4),
                'severe_negative_va_rate': round(float(severe_neg_rate), 4),
                'downside_risk_composite': round(float(0.5 * early_out_rate + 0.5 * collapse_rate), 4)
            })
        return pd.DataFrame(records)

    else:
        # Bowler Downside Metrics
        # Aggregate by over to find expensive spells and blowout overs
        over_stats = df.groupby(['match_id', 'innings', 'bowler_id', 'overid']).agg(
            runs_conceded=('runs_on_delivery', 'sum'),
            boundaries_conceded=('is_four', lambda s: (s | df.loc[s.index, 'is_six']).sum()),
            is_death=('overid', lambda s: (s.iloc[0] >= 15)),
            had_pressure=('is_high_pressure', lambda s: s.any())
        ).reset_index()
        
        # Blowout over: conceding 15+ runs
        over_stats['is_blowout_over'] = (over_stats['runs_conceded'] >= 15).astype(int)
        # Boundary burst over: 2+ boundaries
        over_stats['is_boundary_burst'] = (over_stats['boundaries_conceded'] >= 2).astype(int)
        # Death over failure: overs 18-20 conceding > 12 runs
        over_stats['is_death_failure'] = ((over_stats['overid'] >= 17) & (over_stats['runs_conceded'] >= 13)).astype(int)
        
        records = []
        for p_id, g in over_stats.groupby('bowler_id'):
            overs_count = len(g)
            blowout_rate = g['is_blowout_over'].mean()
            burst_rate = g['is_boundary_burst'].mean()
            death_overs = g[g['is_death']]
            death_fail_rate = death_overs['is_death_failure'].mean() if len(death_overs) > 0 else 0.0
            
            records.append({
                'player_id': p_id,
                'role': 'bowler',
                'blowout_over_rate': round(float(blowout_rate), 4),
                'boundary_burst_rate': round(float(burst_rate), 4),
                'death_failure_rate': round(float(death_fail_rate), 4),
                'downside_risk_composite': round(float(0.5 * blowout_rate + 0.5 * burst_rate), 4)
            })
        return pd.DataFrame(records)
