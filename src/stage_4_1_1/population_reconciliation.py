"""
PinkOps — Stage 4.1.1: Population Reconciliation Ledger
Module: src/stage_4_1_1/population_reconciliation.py

Purpose:
- Provide exact, auditable accounting of the delivery universe across all stages.
- Reconciles 200,999 raw competition deliveries with the 200,961 normal-innings modeling population.
- Formally records Super Over delivery counts (38 balls across 6 matches).
- Exports: data/processed/stage_4_1_1_population_reconciliation.csv
"""

import pandas as pd
from pathlib import Path


def run_population_reconciliation(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    out_csv = project_root / "data" / "processed" / "stage_4_1_1_population_reconciliation.csv"
    
    print(f"Loading match_state from {parquet_path}...")
    df = pd.read_parquet(parquet_path, columns=['match_id', 'innings', 'is_super_over', 'is_legal_delivery'])
    
    raw_total = len(df)
    so_total = int(df['is_super_over'].sum())
    normal_total = raw_total - so_total
    
    inn1_total = int(((df['innings'] == 1) & (df['is_super_over'] == 0)).sum())
    inn2_total = int(((df['innings'] == 2) & (df['is_super_over'] == 0)).sum())
    
    so_inn3 = int((df['innings'] == 3).sum())
    so_inn4 = int((df['innings'] == 4).sum())
    
    matches_total = df['match_id'].nunique()
    so_matches = df[df['is_super_over'] == 1]['match_id'].nunique()
    normal_matches = df[df['is_super_over'] == 0]['match_id'].nunique()
    
    records = [
        {"metric": "Raw Total Deliveries", "count": raw_total, "pct_of_total": 100.0, "status": "Immutable Raw Denominator"},
        {"metric": "Super Over Deliveries (Innings 3 & 4)", "count": so_total, "pct_of_total": round(so_total / raw_total * 100.0, 4), "status": "Isolated in Dedicated Stress Register"},
        {"metric": "Super Over Innings 3 Balls", "count": so_inn3, "pct_of_total": round(so_inn3 / raw_total * 100.0, 4), "status": "Isolated"},
        {"metric": "Super Over Innings 4 Balls", "count": so_inn4, "pct_of_total": round(so_inn4 / raw_total * 100.0, 4), "status": "Isolated"},
        {"metric": "Canonical Normal-Innings Modeling Universe", "count": normal_total, "pct_of_total": round(normal_total / raw_total * 100.0, 4), "status": "Frozen Modeling Denominator"},
        {"metric": "Normal First-Innings Deliveries (Innings 1)", "count": inn1_total, "pct_of_total": round(inn1_total / raw_total * 100.0, 4), "status": "Target Setting Phase"},
        {"metric": "Normal Second-Innings Deliveries (Innings 2)", "count": inn2_total, "pct_of_total": round(inn2_total / raw_total * 100.0, 4), "status": "Chasing Phase"},
        {"metric": "Contested Matches with Delivery Telemetry", "count": matches_total, "pct_of_total": 100.0, "status": "Verified Matches"},
        {"metric": "Matches Involving Super Overs", "count": so_matches, "pct_of_total": round(so_matches / matches_total * 100.0, 4), "status": "Tied Contests (6 Matches)"}
    ]
    
    rec_df = pd.DataFrame(records)
    rec_df.to_csv(out_csv, index=False)
    print(f"Saved population reconciliation to {out_csv}")
    print(rec_df.to_string(index=False))
    
    # Assertions
    assert raw_total == 200999, f"Expected 200,999 raw, got {raw_total}"
    assert so_total == 38, f"Expected 38 Super Over, got {so_total}"
    assert normal_total == 200961, f"Expected 200,961 normal, got {normal_total}"
    assert inn1_total == 105727, f"Expected 105,727 Innings 1, got {inn1_total}"
    assert inn2_total == 95234, f"Expected 95,234 Innings 2, got {inn2_total}"
    assert inn1_total + inn2_total == normal_total, "Innings 1 + 2 != normal total"
    assert so_inn3 + so_inn4 == so_total, "SO Inn 3 + 4 != SO total"
    assert matches_total == 867, f"Expected 867 matches, got {matches_total}"
    assert so_matches == 6, f"Expected 6 SO matches, got {so_matches}"
    
    print("[ALL POPULATION RECONCILIATION INVARIANTS PASS]")
    return rec_df


if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parents[2]
    run_population_reconciliation(proj_root)
