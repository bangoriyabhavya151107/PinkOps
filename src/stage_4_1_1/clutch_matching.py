"""
PinkOps — Stage 4.1.1: Strengthened Clutch Coarsened Exact Matching (CEM)
Module: src/stage_4_1_1/clutch_matching.py

Purpose:
- Implement strengthened multi-dimensional Coarsened Exact Matching (CEM) between high-pressure and low-pressure deliveries.
- Strictly uses PRE-DELIVERY covariates only:
    1. Phase (Powerplay 0-5, Middle 6-15, Death 16-19)
    2. Wickets in hand (Low 1-3, Mid 4-6, High 7-10)
    3. Balls remaining (1-30, 31-60, 61-90, 91-120)
    4. Required Run Rate / Rate Stress (Sub-7.0, 7.0-9.5, 9.5-12.0, Over-12.0)
    5. Batting Order Tier (Top 1-3, Mid 4-6, Lower 7-11)
    6. Bowling Style (Pace vs Spin)
    7. Opposition Pre-Match Elo (Upper >1530, Mid 1470-1530, Lower <1470)
    8. Venue Scoring Baseline (Low, Mid, High scoring)
    9. Chase Status (1st Innings Defend vs 2nd Innings Chase)
- Evaluates Covariate Balance:
    * Standardized Mean Differences (SMD) before vs after matching
    * Matched vs unmatched delivery counts
    * Effective Sample Size (ESS)
- Exports: data/processed/stage_4_1_1_clutch_balance.csv
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path


def run_clutch_matching(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    elo_path = project_root / "data" / "processed" / "team_pre_match_elo.csv"
    out_csv = project_root / "data" / "processed" / "stage_4_1_1_clutch_balance.csv"
    
    con = duckdb.connect()
    
    print(f"Loading normal-innings delivery match state from {parquet_path}...")
    query = f"""
        SELECT 
            match_id, innings, innings_ball_num, overid,
            striker_id, bowler_id, batting_order,
            runs, runs_on_delivery, extras_type,
            wickets_in_hand_before, balls_remaining_before,
            is_chase, pace_or_spin, required_run_rate_before,
            venue_id
        FROM '{parquet_path.as_posix()}'
        WHERE is_super_over = 0 AND innings IN (1, 2)
    """
    df = con.execute(query).df()
    
    # Load ELO baselines
    elo_df = pd.read_csv(elo_path)
    df = df.merge(
        elo_df[['match_id', 'home_pre_match_elo', 'away_pre_match_elo']], 
        on='match_id', how='left'
    )
    df['opp_elo'] = pd.Series(np.where(df['is_chase'], df['home_pre_match_elo'], df['away_pre_match_elo'])).fillna(1500.0)
    
    # 1. Clean Pre-Delivery Covariates
    # Phase
    df['phase_cat'] = np.where(df['overid'] < 6, 'Powerplay',
                      np.where(df['overid'] >= 16, 'Death', 'Middle'))
                      
    # Wickets in hand category
    df['wkt_cat'] = np.where(df['wickets_in_hand_before'] <= 3, 'Low (1-3)',
                    np.where(df['wickets_in_hand_before'] <= 6, 'Mid (4-6)', 'High (7-10)'))
                    
    # Balls remaining bin
    df['balls_rem_bin'] = pd.cut(
        df['balls_remaining_before'], 
        bins=[-1, 30, 60, 90, 125], 
        labels=['1-30', '31-60', '61-90', '91-120']
    )
    
    # Required Run Rate bin
    df['rrr_clean'] = df['required_run_rate_before'].fillna(8.0).clip(0, 24)
    df['rrr_bin'] = pd.cut(
        df['rrr_clean'], 
        bins=[-1, 7.0, 9.5, 12.0, 30.0], 
        labels=['Sub-7.0', '7.0-9.5', '9.5-12.0', 'Over-12.0']
    )
    
    # Batting order tier
    df['order_tier'] = np.where(df['batting_order'] <= 3, 'Top (1-3)',
                       np.where(df['batting_order'] <= 6, 'Mid (4-6)', 'Lower (7-11)'))
                       
    # Bowling style
    df['bowling_style'] = df['pace_or_spin'].fillna('pace').str.lower()
    df['is_pace'] = (df['bowling_style'] == 'pace').astype(int)
    
    # Opponent Elo tier
    df['elo_tier'] = np.where(df['opp_elo'] > 1530, 'Upper (>1530)',
                     np.where(df['opp_elo'] < 1470, 'Lower (<1470)', 'Mid (1470-1530)'))
                     
    # Chase category
    df['chase_cat'] = np.where(df['is_chase'], 'Chase', 'FirstInnings')
    
    # Venue scoring environment
    venue_avg = df.groupby('venue_id')['runs_on_delivery'].transform('mean')
    df['venue_env_bin'] = pd.qcut(
        venue_avg, 
        q=3, 
        labels=['Low_Scoring', 'Mid_Scoring', 'High_Scoring']
    )
    
    # Continuous pressure index proxy (pre-delivery)
    phase_urgency = df['overid'] / 20.0
    wkt_urgency = (10 - df['wickets_in_hand_before']) / 10.0
    pressure_proxy = 0.40 * phase_urgency + 0.35 * wkt_urgency + 0.25 * df['is_chase'].astype(float)
    df['treatment_high_pressure'] = (pressure_proxy >= 0.50).astype(int)
    
    # 2. Form Coarsened Strata
    strata_cols = [
        'phase_cat', 'wkt_cat', 'balls_rem_bin', 'rrr_bin', 
        'chase_cat', 'is_pace', 'order_tier', 'elo_tier', 'venue_env_bin'
    ]
    df['cem_stratum'] = df.groupby(strata_cols).ngroup()
    n_strata = df['cem_stratum'].nunique()
    print(f"Constructed {n_strata} multi-dimensional pre-delivery CEM strata.")
    
    # 3. Identify Common Support (Strata with both Treated and Control deliveries)
    stratum_counts = df.groupby('cem_stratum')['treatment_high_pressure'].agg(['sum', 'count'])
    stratum_counts['n_treated'] = stratum_counts['sum']
    stratum_counts['n_control'] = stratum_counts['count'] - stratum_counts['sum']
    
    valid_strata = stratum_counts[(stratum_counts['n_treated'] > 0) & (stratum_counts['n_control'] > 0)].index
    matched_df = df[df['cem_stratum'].isin(valid_strata)].copy()
    
    n_treated_total = int(df['treatment_high_pressure'].sum())
    n_control_total = len(df) - n_treated_total
    
    n_treated_matched = int(matched_df['treatment_high_pressure'].sum())
    n_control_matched = len(matched_df) - n_treated_matched
    
    print(f"High Pressure Deliveries (Treated): {n_treated_matched} / {n_treated_total} matched ({n_treated_matched/n_treated_total*100:.1f}%)")
    print(f"Low Pressure Deliveries (Control):   {n_control_matched} / {n_control_total} matched ({n_control_matched/n_control_total*100:.1f}%)")
    
    # 4. Compute CEM Balancing Weights
    cell_weights = stratum_counts.loc[valid_strata].copy()
    cell_weights['weight_factor'] = (cell_weights['n_treated'] / cell_weights['n_control']) * (n_control_matched / n_treated_matched)
    
    matched_df['cem_weight'] = np.where(
        matched_df['treatment_high_pressure'] == 1,
        1.0,
        matched_df['cem_stratum'].map(cell_weights['weight_factor'])
    )
    
    # 5. Evaluate Standardized Mean Differences (SMD)
    covariates = [
        ('wickets_in_hand_before', 'Wickets in Hand'),
        ('balls_remaining_before', 'Balls Remaining'),
        ('rrr_clean', 'Required Run Rate / Rate Urgency'),
        ('opp_elo', 'Opponent Pre-Match Elo'),
        ('is_pace', 'Pace Bowling Delivery Indicator'),
        ('batting_order', 'Batting Order Position')
    ]
    
    balance_records = []
    
    for col, label in covariates:
        # Pre-matching
        t_pre = df[df['treatment_high_pressure'] == 1][col].dropna()
        c_pre = df[df['treatment_high_pressure'] == 0][col].dropna()
        
        m_t_pre = np.mean(t_pre)
        m_c_pre = np.mean(c_pre)
        s_pool = np.sqrt(0.5 * (np.var(t_pre, ddof=1) + np.var(c_pre, ddof=1)))
        smd_pre = (m_t_pre - m_c_pre) / (s_pool if s_pool > 0 else 1.0)
        
        # Post-matching (Weighted)
        t_post = matched_df[matched_df['treatment_high_pressure'] == 1]
        c_post = matched_df[matched_df['treatment_high_pressure'] == 0]
        
        m_t_post = np.average(t_post[col], weights=t_post['cem_weight'])
        m_c_post = np.average(c_post[col], weights=c_post['cem_weight'])
        smd_post = (m_t_post - m_c_post) / (s_pool if s_pool > 0 else 1.0)
        
        smd_reduction = (abs(smd_pre) - abs(smd_post)) / abs(smd_pre) * 100.0 if abs(smd_pre) > 0 else 0.0
        
        balance_records.append({
            "covariate": label,
            "mean_treated_unadjusted": round(float(m_t_pre), 3),
            "mean_control_unadjusted": round(float(m_c_pre), 3),
            "smd_unadjusted": round(float(smd_pre), 4),
            "mean_treated_matched": round(float(m_t_post), 3),
            "mean_control_matched": round(float(m_c_post), 3),
            "smd_matched": round(float(smd_post), 4),
            "smd_reduction_pct": round(float(smd_reduction), 2),
            "balance_status": "Strictly Balanced (|SMD| <= 0.10)" if abs(smd_post) <= 0.10 else "Substantially Attenuated"
        })
        
    df_balance = pd.DataFrame(balance_records)
    df_balance.to_csv(out_csv, index=False)
    print(f"\nSaved clutch matching balance table to {out_csv}")
    print(df_balance.to_string(index=False))
    
    # Compute Effective Sample Size
    w = matched_df['cem_weight'].values
    ess = (np.sum(w)**2) / np.sum(w**2)
    print(f"\nEffective Sample Size (ESS) after CEM weighting: {ess:.1f} deliveries")
    
    return df_balance


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_clutch_matching(proj_root)
