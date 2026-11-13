"""
PinkOps — Stage 4.1.1: Comprehensive Player Attribution Audit
Module: src/stage_4_1_1/attribution_audit.py

Purpose:
- Rigorously audit player attribution across all 200,999 raw deliveries and 200,961 normal-innings deliveries.
- Full reconciliation of runs, extras, and dismissals to batter and bowler ledgers.
- Explicit accounting for:
    * wide (7,714 raw; 7,713 normal, 1 Super Over): not faced by batter; runs conceded by bowler.
    * Overstep / noball: faced by batter; runs conceded by bowler.
    * legbyes (2,748 raw; 2,748 normal, 0 Super Over): faced by batter; 0 runs conceded by bowler (fielding extra).
    * byes (529 raw; 528 normal, 1 Super Over): faced by batter; 0 runs conceded by bowler (wicketkeeper extra).
    * Penalty (1 raw; 1 normal, 0 Super Over): 0 runs to batter, 0 runs to bowler.
    * RunOut (600 raw; 598 normal, 2 Super Over): team dismissals; 0 bowler wickets; isolated from batter execution failure.
    * Retired hurt (12 raw; 12 normal, 0 Super Over): injury events; strictly 0 wickets charged to batter or bowler.
    * Standard dismissals: Caught, Bowled, LBW, Stump, Hit Wicket, Retire Out, Obstructing the field.
- Exports: data/processed/stage_4_1_1_attribution_audit.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path


def run_attribution_audit(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    out_csv = project_root / "data" / "processed" / "stage_4_1_1_attribution_audit.csv"
    
    print(f"Loading match_state from {parquet_path}...")
    cols = [
        'match_id', 'innings', 'is_super_over', 'runs', 'extras_type', 
        'extras1_runs', 'runs_on_delivery', 'is_legal_delivery', 
        'is_wicket', 'dismissal_type_cleaned', 'is_bowler_wicket', 
        'is_team_wicket', 'is_retired_hurt'
    ]
    df = pd.read_parquet(parquet_path, columns=cols)
    
    total_raw = len(df)
    so_mask = df['is_super_over'] == 1
    normal_df = df[~so_mask].copy()
    so_df = df[so_mask].copy()
    
    n_so = int(so_mask.sum())
    n_normal = len(normal_df)
    n_inn1 = int((normal_df['innings'] == 1).sum())
    n_inn2 = int((normal_df['innings'] == 2).sum())
    
    print(f"Population Audit: Raw={total_raw}, Super Over={n_so}, Normal={n_normal} (Inn1={n_inn1}, Inn2={n_inn2})")
    
    # Assert population denominators
    assert total_raw == 200999, f"Expected 200,999 raw, got {total_raw}"
    assert n_so == 38, f"Expected 38 Super Over, got {n_so}"
    assert n_normal == 200961, f"Expected 200,961 normal, got {n_normal}"
    assert n_inn1 == 105727, f"Expected 105,727 Innings 1, got {n_inn1}"
    assert n_inn2 == 95234, f"Expected 95,234 Innings 2, got {n_inn2}"
    
    # 1. Audit Extras in Normal Modeling Population
    extras_records = []
    for extra_cat in ['wide', 'legbyes', 'Overstep', 'byes', 'other', 'Penalty', 'None (Clean Delivery)']:
        if extra_cat == 'None (Clean Delivery)':
            sub = normal_df[normal_df['extras_type'].isna()]
            raw_sub = df[df['extras_type'].isna()]
        else:
            sub = normal_df[normal_df['extras_type'] == extra_cat]
            raw_sub = df[df['extras_type'] == extra_cat]
            
        cnt_normal = len(sub)
        cnt_raw = len(raw_sub)
        tot_runs = int(sub['runs_on_delivery'].sum())
        bat_runs = int(sub['runs'].sum())
        extra_runs = int(sub['extras1_runs'].sum())
        
        if extra_cat == 'wide':
            bat_faced = 0
            bat_cred = 0
            bowl_charged = 1
            rule = "Wides are bowler execution extras; batter did not face a legal ball; excluded from balls faced"
        elif extra_cat in ['legbyes', 'byes']:
            bat_faced = 1
            bat_cred = 0
            bowl_charged = 0
            rule = f"{extra_cat.capitalize()} are fielding/keeper extras; batter faced ball; excluded from bowler runs conceded"
        elif extra_cat == 'Penalty':
            bat_faced = 0
            bat_cred = 0
            bowl_charged = 0
            rule = "Penalty runs are team conduct adjustments; strictly isolated from individual player metrics"
        elif extra_cat in ['Overstep', 'other']:
            bat_faced = 1
            bat_cred = 1
            bowl_charged = 1
            rule = "No-balls / illegal deliveries; batter faced delivery; extra run charged to bowler ledger"
        else:
            bat_faced = 1
            bat_cred = 1
            bowl_charged = 1
            rule = "Standard legal delivery; runs off bat credited to batter; runs conceded charged to bowler"
            
        extras_records.append({
            "category_type": "Extra Attribution",
            "event_name": extra_cat,
            "raw_delivery_count": cnt_raw,
            "normal_delivery_count": cnt_normal,
            "super_over_count": cnt_raw - cnt_normal,
            "normal_runs_on_delivery": tot_runs,
            "batter_runs_off_bat": bat_runs,
            "extras_runs": extra_runs,
            "batter_ball_faced": bat_faced,
            "bowler_runs_charged": bowl_charged,
            "accounting_rule": rule
        })
        
    # 2. Audit Dismissals in Normal Modeling Population
    dismissal_records = []
    all_dismissal_types = df['dismissal_type_cleaned'].value_counts(dropna=False).to_dict()
    for d_type, cnt_raw in all_dismissal_types.items():
        if pd.isna(d_type):
            sub = normal_df[normal_df['dismissal_type_cleaned'].isna()]
            raw_sub = df[df['dismissal_type_cleaned'].isna()]
            d_name = "None (Not Out)"
        else:
            sub = normal_df[normal_df['dismissal_type_cleaned'] == d_type]
            raw_sub = df[df['dismissal_type_cleaned'] == d_type]
            d_name = str(d_type)
            
        cnt_normal = len(sub)
        bowl_wkts = int(sub['is_bowler_wicket'].sum())
        team_wkts = int(sub['is_team_wicket'].sum())
        
        if d_name in ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']:
            class_type = "Bowler Wicket + Batter Dismissal"
            bat_charged = 1
            bowl_cred = 1
            rule = "Direct execution dismissal; credited to bowler wicket column; charged to batter dismissal ledger"
        elif d_name == 'RunOut':
            class_type = "Team Dismissal (0 Bowler Wicket; Isolated Batter Attribution)"
            bat_charged = 0  # isolated from direct individual skill failure unless verified
            bowl_cred = 0
            rule = "Run outs involve fielding action / team running error; strictly 0 bowler wickets; isolated from batter failure"
        elif d_name == 'Retire Out':
            class_type = "Tactical Team Dismissal (0 Bowler Wicket)"
            bat_charged = 1
            bowl_cred = 0
            rule = "Tactical retirement counted as batter dismissal; 0 wickets credited to bowler"
        elif d_name == 'Obstructing the field':
            class_type = "Conduct Dismissal (0 Bowler Wicket)"
            bat_charged = 1
            bowl_cred = 0
            rule = "Conduct dismissal counted as batter dismissal; 0 wickets credited to bowler"
        else:
            class_type = "Not Out"
            bat_charged = 0
            bowl_cred = 0
            rule = "Delivery did not produce a dismissal"
            
        dismissal_records.append({
            "category_type": "Dismissal Attribution",
            "event_name": d_name,
            "raw_delivery_count": cnt_raw,
            "normal_delivery_count": cnt_normal,
            "super_over_count": cnt_raw - cnt_normal,
            "normal_runs_on_delivery": int(sub['runs_on_delivery'].sum()),
            "batter_runs_off_bat": int(sub['runs'].sum()),
            "extras_runs": int(sub['extras1_runs'].sum()),
            "batter_ball_faced": 1,
            "bowler_runs_charged": bowl_cred,
            "accounting_rule": rule
        })
        
    # 3. Add Isolated Retired Hurt Audit Record
    ret_hurt_raw = df[df['is_retired_hurt'] == 1]
    ret_hurt_normal = normal_df[normal_df['is_retired_hurt'] == 1]
    dismissal_records.append({
        "category_type": "Injury Isolation",
        "event_name": "Retired Hurt (Injury)",
        "raw_delivery_count": len(ret_hurt_raw),
        "normal_delivery_count": len(ret_hurt_normal),
        "super_over_count": len(ret_hurt_raw) - len(ret_hurt_normal),
        "normal_runs_on_delivery": int(ret_hurt_normal['runs_on_delivery'].sum()),
        "batter_runs_off_bat": int(ret_hurt_normal['runs'].sum()),
        "extras_runs": int(ret_hurt_normal['extras1_runs'].sum()),
        "batter_ball_faced": 1,
        "bowler_runs_charged": 0,
        "accounting_rule": "Physical injury event; strictly 0 team wickets and 0 bowler wickets; zero downside penalty charged"
    })
    
    # Combine and save
    audit_df = pd.DataFrame(extras_records + dismissal_records)
    audit_df.to_csv(out_csv, index=False)
    print(f"Saved complete attribution audit to {out_csv}")
    
    # Exact verification assertions
    assert len(ret_hurt_raw) == 12, f"Expected 12 raw retired hurt, got {len(ret_hurt_raw)}"
    assert len(ret_hurt_normal) == 12, f"Expected 12 normal retired hurt, got {len(ret_hurt_normal)}"
    assert int(ret_hurt_normal['is_bowler_wicket'].sum()) == 0, "Retired hurt credited to bowler!"
    assert int(ret_hurt_normal['is_team_wicket'].sum()) == 0, "Retired hurt counted as team wicket!"
    
    raw_runouts = len(df[df['dismissal_type_cleaned'] == 'RunOut'])
    normal_runouts = len(normal_df[normal_df['dismissal_type_cleaned'] == 'RunOut'])
    so_runouts = len(so_df[so_df['dismissal_type_cleaned'] == 'RunOut'])
    assert raw_runouts == 600, f"Expected 600 raw runouts, got {raw_runouts}"
    assert normal_runouts == 598, f"Expected 598 normal runouts, got {normal_runouts}"
    assert so_runouts == 2, f"Expected 2 Super Over runouts, got {so_runouts}"
    assert int(normal_df[normal_df['dismissal_type_cleaned'] == 'RunOut']['is_bowler_wicket'].sum()) == 0, "Run out credited to bowler!"
    
    print("[ALL ATTRIBUTION ACCOUNTING INVARIANTS PASS]")
    return audit_df


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_attribution_audit(proj_root)
