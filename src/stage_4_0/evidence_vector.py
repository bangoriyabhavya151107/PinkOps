"""
PinkOps — Stage 4.0: Player Evidence Vector Schema Assembly Module
Module: src/stage_4_0/evidence_vector.py

Purpose:
- Assemble the formal uncollapsed 7-layer Player Evidence Vector.
- Enforce strict governance: Zero composite ranking, zero Top 10 lists, zero arbitrary weights.
- Output clean, structured evidence vectors for batters and bowlers separately.
"""

import pandas as pd
import numpy as np


def build_evidence_vector(
    exposure_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    downside_df: pd.DataFrame,
    consistency_df: pd.DataFrame,
    clutch_df: pd.DataFrame,
    uncertainty_df: pd.DataFrame,
    context_df: pd.DataFrame,
    stability_df: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Assembles the frozen Player Evidence Vector schema across the 7 governance layers:
    1. Opportunity Layer
    2. Expectation Layer
    3. Execution Layer
    4. Reliability Layer
    5. Evidence Layer
    6. Context Layer
    7. Robustness Layer
    """
    # Merge all modular layers on (player_id, role)
    merged = exposure_df.merge(attribution_df, on=['player_id', 'role'], how='inner')
    merged = merged.merge(downside_df, on=['player_id', 'role'], how='left')
    merged = merged.merge(consistency_df, on=['player_id', 'role'], how='left')
    merged = merged.merge(clutch_df, on=['player_id', 'role'], how='left')
    
    # Merge uncertainty columns
    u_cols = ['player_id', 'role', 'shrinkage_weight', 'posterior_mean', 'posterior_se', 'ci_95_width', 'lcb_20', 'lcb_10', 'lcb_25', 'lcb_30']
    merged = merged.merge(uncertainty_df[u_cols], on=['player_id', 'role'], how='left')
    
    # Merge context columns (opponent elo, role details)
    if context_df is not None:
        merged = merged.merge(context_df, on=['player_id', 'role'], how='left')
        
    # Merge specification stability if provided
    if stability_df is not None:
        merged = merged.merge(stability_df, on=['player_id', 'role'], how='left')
    else:
        merged['specification_stability_pct'] = np.where(merged['posterior_mean'] > 0, 100.0, 0.0)

    # Formal frozen column schema ordering
    schema_cols = [
        # Player Identity
        'player_id', 'role',
        
        # 1. Opportunity Layer
        'total_opportunities', 'pressure_opportunities', 'weighted_pressure_exposure', 
        'pressure_exposure_pct', 'evidence_tier',
        
        # 2. Expectation Layer
        'expected_performance_mean',
        
        # 3. Execution Layer
        'actual_performance_mean', 'raw_va_per_ball', 'pressure_va_per_ball',
        'boundary_execution_rate', 'dot_execution_rate', 'wicket_execution_rate', 'strike_rotation_rate',
        
        # 4. Reliability Layer (Downside & Consistency)
        'downside_risk_composite', 'consistency_mad', 'consistency_iqr', 'negative_match_pct', 'floor_va_p10',
        
        # 5. Evidence Layer (Posterior & Uncertainty)
        'posterior_mean', 'posterior_se', 'ci_95_width', 'lcb_20',
        
        # 6. Context Layer
        'clutch_delta_matched', 'matching_coverage_pct',
        'opponent_avg_elo', 'role_avg_batting_order',
        
        # 7. Robustness Layer
        'specification_stability_pct'
    ]
    
    final_cols = [c for c in schema_cols if c in merged.columns]
    evidence_vector = merged[final_cols].copy()
    
    # Assertions: No ranking columns permitted
    assert 'rank' not in evidence_vector.columns, "Governance Violation: rank column detected!"
    assert 'pinkops_score' not in evidence_vector.columns, "Governance Violation: composite score detected!"
    assert 'composite_score' not in evidence_vector.columns, "Governance Violation: composite score detected!"
    
    return evidence_vector
