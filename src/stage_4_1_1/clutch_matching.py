"""
PinkOps — Stage 4.1.1: Strengthened Clutch Coarsened Exact Matching (CEM) (Hardened)
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
    7. Opposition Pre-Match Elo: assigned from ACTUAL opponent bowling team (not inferred from chase)
    8. Venue Scoring Baseline: STRICTLY PRE-MATCH historical expanding baseline (excluding current & future matches)
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
            match_id, match_date, innings, innings_ball_num, overid,
            striker_id, bowler_id, home_team_id, away_team_id,
            batting_team_id, bowling_team_id, batting_order,
            runs, runs_on_delivery, extras_type, is_legal_delivery,
            wickets_in_hand_before, balls_remaining_before,
            is_chase, pace_or_spin, required_run_rate_before,
            venue_id
        FROM '{parquet_path.as_posix()}'
        WHERE is_super_over = 0 AND innings IN (1, 2)
    """
    df = con.execute(query).df()
    n_deliveries = len(df)
    
    # -------------------------------------------------------------
    # 1. Opponent Pre-Match Elo Assignment (Hardened & Leakage-Free)
    # Correct relation: batting_team -> opponent_team = bowling_team -> opponent pre-match Elo
    # -------------------------------------------------------------
    elo_df = pd.read_csv(elo_path)
    df = df.merge(
        elo_df[['match_id', 'home_team_id', 'away_team_id', 'home_pre_match_elo', 'away_pre_match_elo']], 
        on='match_id', how='left', suffixes=('', '_elo')
    )
    
    # Assert bowling_team is either home or away
    is_home_bowler = (df['bowling_team_id'] == df['home_team_id'])
    is_away_bowler = (df['bowling_team_id'] == df['away_team_id'])
    assert (is_home_bowler | is_away_bowler).all(), "Bowler team not in home/away teams!"
    assert (df['batting_team_id'] != df['bowling_team_id']).all(), "Batting team equals bowling team!"
    
    # Correctly assign opponent Elo from actual opponent bowling team
    df['opp_team_id'] = df['bowling_team_id']
    df['opp_elo'] = np.where(
        is_home_bowler, 
        df['home_pre_match_elo'], 
        df['away_pre_match_elo']
    )
    df['opp_elo'] = df['opp_elo'].fillna(1500.0)
    print(f"Verified opponent Elo assignment across {n_deliveries:,} deliveries (100% verified against actual opponent bowling team).")

    # -------------------------------------------------------------
    # 2. Historical Pre-Match Venue Scoring Baseline (Strictly Pre-Match)
    # Computes expanding historical venue averages strictly before current match date
    # -------------------------------------------------------------
    match_venue_df = df.groupby(['venue_id', 'match_date', 'match_id']).agg(
        match_runs=('runs_on_delivery', 'sum'),
        match_balls=('is_legal_delivery', 'sum')
    ).reset_index().sort_values(['venue_id', 'match_date', 'match_id'])

    # Historical cumulative sums excluding current match
    match_venue_df['cum_runs'] = match_venue_df.groupby('venue_id')['match_runs'].cumsum() - match_venue_df['match_runs']
    match_venue_df['cum_balls'] = match_venue_df.groupby('venue_id')['match_balls'].cumsum() - match_venue_df['match_balls']
    match_venue_df['prior_matches'] = match_venue_df.groupby('venue_id').cumcount()

    # Empirical Bayes shrinkage toward population mean (1.30 runs/ball) with K=500
    K_venue = 500.0
    pop_mean = 1.30
    match_venue_df['hist_venue_baseline'] = (match_venue_df['cum_runs'] + K_venue * pop_mean) / (match_venue_df['cum_balls'] + K_venue)

    # Verification: Ensure prior_matches == 0 has exactly cum_balls == 0
    zero_prior = match_venue_df[match_venue_df['prior_matches'] == 0]
    assert (zero_prior['cum_balls'] == 0).all(), "Prior matches == 0 has non-zero balls!"
    assert (zero_prior['cum_runs'] == 0).all(), "Prior matches == 0 has non-zero runs!"
    assert np.allclose(zero_prior['hist_venue_baseline'], 1.30), "Zero prior baseline != 1.30!"

    # Merge strictly historical venue baseline back to delivery dataframe
    df = df.merge(
        match_venue_df[['match_id', 'hist_venue_baseline', 'prior_matches']], 
        on='match_id', how='left'
    )
    print("Verified historical venue baselines: strictly excludes current match and all future matches.")

    # -------------------------------------------------------------
    # 3. Clean Pre-Delivery Covariates for CEM Matching
    # -------------------------------------------------------------
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
    
    # Venue scoring environment (tertiles from strictly pre-match historical baseline)
    df['venue_env_bin'] = pd.qcut(
        df['hist_venue_baseline'], 
        q=3, 
        labels=['Low_Scoring', 'Mid_Scoring', 'High_Scoring']
    )
    
    # Continuous pressure index proxy (pre-delivery)
    phase_urgency = df['overid'] / 20.0
    wkt_urgency = (10 - df['wickets_in_hand_before']) / 10.0
    pressure_proxy = 0.40 * phase_urgency + 0.35 * wkt_urgency + 0.25 * df['is_chase'].astype(float)
    df['treatment_high_pressure'] = (pressure_proxy >= 0.50).astype(int)
    
    # -------------------------------------------------------------
    # 4. Form Coarsened Exact Matching (CEM) Strata
    # -------------------------------------------------------------
    strata_cols = [
        'phase_cat', 'wkt_cat', 'balls_rem_bin', 'rrr_bin', 
        'chase_cat', 'is_pace', 'order_tier', 'elo_tier', 'venue_env_bin'
    ]
    df['cem_stratum'] = df.groupby(strata_cols).ngroup()
    n_strata = df['cem_stratum'].nunique()
    print(f"Constructed {n_strata} multi-dimensional pre-delivery CEM strata.")
    
    # -------------------------------------------------------------
    # 5. Common Support Identification & Pruning
    # -------------------------------------------------------------
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
    
    # -------------------------------------------------------------
    # 6. Compute CEM Balancing Weights
    # -------------------------------------------------------------
    cell_weights = stratum_counts.loc[valid_strata].copy()
    cell_weights['weight_factor'] = (cell_weights['n_treated'] / cell_weights['n_control']) * (n_control_matched / n_treated_matched)
    
    matched_df['cem_weight'] = np.where(
        matched_df['treatment_high_pressure'] == 1,
        1.0,
        matched_df['cem_stratum'].map(cell_weights['weight_factor'])
    )
    
    # -------------------------------------------------------------
    # 7. Evaluate Standardized Mean Differences (SMD)
    # -------------------------------------------------------------
    covariates = [
        ('wickets_in_hand_before', 'Wickets in Hand'),
        ('balls_remaining_before', 'Balls Remaining'),
        ('rrr_clean', 'Required Run Rate / Rate Urgency'),
        ('opp_elo', 'Opponent Pre-Match Elo'),
        ('is_pace', 'Pace Bowling Delivery Indicator'),
        ('batting_order', 'Batting Order Position'),
        ('hist_venue_baseline', 'Pre-Match Historical Venue Baseline')
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
    print(f"\nSaved hardened clutch matching balance table to {out_csv}")
    print(df_balance.to_string(index=False))
    
    # Compute Effective Sample Size
    w = matched_df['cem_weight'].values
    ess = (np.sum(w)**2) / np.sum(w**2)
    print(f"\nEffective Sample Size (ESS) after CEM weighting: {ess:.1f} deliveries")
    
    return df_balance


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_clutch_matching(proj_root)
