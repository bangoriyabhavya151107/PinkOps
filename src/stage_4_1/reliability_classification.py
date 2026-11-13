"""
PinkOps — Stage 4.1: Reliability Classification Module
Module: src/stage_4_1/reliability_classification.py

Purpose:
- Classify players into transparent, evidence-based Decision Profiles
  without collapsing the multi-dimensional vector into an arbitrary single score.
- Profiles:
  1. Reliable Pressure Performer (Strong execution + robust evidence + controlled downside)
  2. High-Upside / Higher-Risk (Strong execution + elevated downside / high volatility)
  3. Context Specialist (Strong execution concentrated in specific phase/role)
  4. Emerging Evidence (Moderate exposure + promising positive execution)
  5. Pressure Concern (Negative execution or severe downside supported by evidence)
  6. Neutral / Insufficient Evidence (Sparse exposure or near-zero execution)
- Exports: data/processed/stage_4_1_player_classifications.csv
"""

import pandas as pd
import numpy as np


def classify_player_reliability(df_evidence: pd.DataFrame) -> pd.DataFrame:
    """
    Applies explicit, auditable governance rules to classify players into evidence profiles.
    """
    df = df_evidence.copy()
    
    profiles = []
    classification_reasons = []
    
    for idx, row in df.iterrows():
        tier = str(row['evidence_tier']).replace(' Evidence', '').strip()
        eb = row['eb_shrunk_estimate']
        lub20 = row['lub_20']
        downside = row['early_dismissal_rate'] # EDR for batters, BOR for bowlers
        mad = row['match_va_mad']
        neg_pct = row['negative_match_pct']
        pct_death = row['pct_death']
        pct_pp = row['pct_powerplay']
        n_pr = row['n_deliveries_pressure']
        n_tot = row['n_deliveries_total']
        role = row['role']
        
        downside_cap = 0.20 if role == 'batter' else 0.18
        downside_extreme = 0.35 if role == 'batter' else 0.30
        
        # Rule 1: Pressure Concern (Evidence supported negative execution or extreme downside)
        if (tier in ['Robust', 'Moderate']) and (lub20 < -0.05 or downside >= downside_extreme):
            p = "Pressure Concern"
            r = f"Supported negative execution (LUB20: {lub20:.3f}) or severe downside ({downside*100:.1f}%)"
            
        # Rule 2: Reliable Pressure Performer (Robust evidence, positive LUB20, controlled downside)
        elif (tier == 'Robust') and (lub20 >= 0.02) and (downside <= downside_cap) and (neg_pct <= 0.60):
            p = "Reliable Pressure Performer"
            r = f"Robust evidence (N_pr: {n_pr}), positive LUB20 ({lub20:.3f}), controlled downside ({downside*100:.1f}%)"
            
        # Rule 3: Context Specialist (Strong execution concentrated in Death or Powerplay)
        elif (tier in ['Robust', 'Moderate']) and (lub20 >= 0.00) and ((pct_death >= 0.40) or (pct_pp >= 0.50)):
            phase_name = "Death" if pct_death >= 0.40 else "Powerplay"
            p = "Context Specialist"
            r = f"High phase concentration in {phase_name} ({max(pct_death, pct_pp)*100:.1f}%) with non-negative LUB20 ({lub20:.3f})"
            
        # Rule 4: High-Upside / Higher-Risk (Strong point execution but elevated downside or volatility)
        elif (tier in ['Robust', 'Moderate']) and (eb >= 0.05) and (downside > downside_cap or mad >= 0.60 or neg_pct > 0.60):
            p = "High-Upside / Higher-Risk"
            r = f"Strong EB point execution ({eb:.3f}) with elevated downside ({downside*100:.1f}%) or volatility (MAD: {mad:.2f})"
            
        # Rule 5: Emerging Evidence (Moderate tier, promising execution)
        elif (tier == 'Moderate') and (eb >= 0.02) and (downside <= downside_cap + 0.05):
            p = "Emerging Evidence"
            r = f"Moderate evidence (N_pr: {n_pr}) with positive trend (EB: {eb:.3f})"
            
        # Rule 6: Neutral / Insufficient Evidence
        else:
            p = "Neutral / Insufficient Evidence"
            if tier == 'Sparse':
                r = f"Sparse exposure (Total: {n_tot}, Pressure: {n_pr}); high epistemic uncertainty"
            else:
                r = f"Execution within neutral band (|EB| < 0.02, LUB20: {lub20:.3f})"
                
        profiles.append(p)
        classification_reasons.append(r)
        
    df['reliability_profile'] = profiles
    df['classification_rationale'] = classification_reasons
    
    # Summary of classification distribution
    print("\nReliability Profile Distribution:")
    summary = df.groupby(['role', 'reliability_profile']).size().unstack(fill_value=0)
    print(summary.to_string())
    
    return df
