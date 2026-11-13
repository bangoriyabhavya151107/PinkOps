"""
PinkOps — Stage 4.1: Role Analysis Module
Module: src/stage_4_1/role_analysis.py

Purpose:
- Segment player evaluations into specific tactical roles relevant to Rajasthan Royals.
- Prevents cross-role conflation (e.g. comparing an opening powerplay accumulator to a death finisher).
- Roles:
  - Batters:
    1. Top-Order Anchor / Enforcer (Order 1-3, high Powerplay exposure)
    2. Middle-Overs Controller / Accelerator (Order 4-6, high Middle exposure)
    3. Death Finisher (Order 5-8, high Death exposure >= 30%)
  - Bowlers:
    1. Powerplay Specialist (Powerplay overs >= 40%)
    2. Middle Enforcer (Middle overs >= 50%)
    3. Death Specialist (Death overs >= 35%)
    - Sub-segmented by Pace vs Spin.
"""

import pandas as pd
import numpy as np


def assign_tactical_roles(df_evidence: pd.DataFrame) -> pd.DataFrame:
    """Assigns deterministic, data-driven tactical roles to batters and bowlers."""
    df = df_evidence.copy()
    
    tactical_roles = []
    for idx, row in df.iterrows():
        role = row['role']
        pp = row['pct_powerplay']
        death = row['pct_death']
        mid = 1.0 - (pp + death)
        pace = row['pct_vs_pace']
        
        if role == 'batter':
            if death >= 0.28:
                t_role = "Finisher / Death Specialist"
            elif pp >= 0.40:
                t_role = "Top-Order Anchor / Powerplay Batter"
            else:
                t_role = "Middle-Overs Accelerator"
        else: # bowler
            bowling_type = "Pace" if pace >= 0.50 else "Spin"
            if death >= 0.30:
                t_role = f"Death Specialist ({bowling_type})"
            elif pp >= 0.38:
                t_role = f"Powerplay Specialist ({bowling_type})"
            else:
                t_role = f"Middle Enforcer ({bowling_type})"
                
        tactical_roles.append(t_role)
        
    df['tactical_role'] = tactical_roles
    
    print("\nTactical Role Breakdown:")
    print(df.groupby(['role', 'tactical_role']).size().to_string())
    
    return df
