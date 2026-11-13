"""
PinkOps — Stage 4.0 Remediation: Population Reconciliation
Module: src/stage_4_0/population_reconciliation.py

Purpose:
- Authoritative reconciliation of all delivery populations:
  - Raw ball-by-ball universe: 200,999 rows
  - Super Over universe: 38 rows (Innings 3 & 4)
  - Normal-innings modeling universe: 200,961 rows (Innings 1 & 2)
- Reconciles across all stage models and subsets.
- Outputs CSV text to stdout for reliable host writing.
"""

import duckdb
import pandas as pd
from pathlib import Path


def run_population_reconciliation(project_root: Path):
    parquet_path = project_root / "data" / "processed" / "match_state.parquet"
    raw_path = project_root / "data" / "raw" / "6af458274c1e8_data_pack" / "Data Pack" / "ball_by_ball.csv"
    
    con = duckdb.connect()
    
    # 1. Raw ball-by-ball counts
    n_raw = con.execute(f"SELECT COUNT(*) FROM '{raw_path}'").fetchone()[0]
    
    # 2. Match state parquet counts by innings
    inn_counts = con.execute(f"""
        SELECT 
            innings,
            COUNT(*) as n_balls,
            COUNT(DISTINCT match_id) as n_matches
        FROM '{parquet_path}'
        GROUP BY innings
        ORDER BY innings
    """).df()
    
    inn_1 = inn_counts.loc[inn_counts['innings'] == 1, 'n_balls'].values[0]
    inn_2 = inn_counts.loc[inn_counts['innings'] == 2, 'n_balls'].values[0]
    inn_3 = inn_counts.loc[inn_counts['innings'] == 3, 'n_balls'].values[0] if 3 in inn_counts['innings'].values else 0
    inn_4 = inn_counts.loc[inn_counts['innings'] == 4, 'n_balls'].values[0] if 4 in inn_counts['innings'].values else 0
    
    n_normal = inn_1 + inn_2
    n_super_over = inn_3 + inn_4
    n_total_parquet = n_normal + n_super_over
    
    # Assertions
    assert n_raw == 200999, f"Raw count mismatch: {n_raw} != 200999"
    assert n_total_parquet == 200999, f"Parquet count mismatch: {n_total_parquet} != 200999"
    assert n_super_over == 38, f"Super Over mismatch: {n_super_over} != 38"
    assert n_normal == 200961, f"Normal modeling mismatch: {n_normal} != 200961"
    assert n_raw - n_super_over == n_normal, "Arithmetic reconciliation failed!"
    
    # Subset counts
    chase_balls = con.execute(f"SELECT COUNT(*) FROM '{parquet_path}' WHERE innings = 2").fetchone()[0]
    chase_rrr_balls = con.execute(f"SELECT COUNT(*) FROM '{parquet_path}' WHERE innings = 2 AND required_run_rate_before IS NOT NULL").fetchone()[0]
    so_matches = con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}' WHERE is_super_over = true").fetchone()[0]
    revised_overs_matches = con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}' WHERE is_overs_revised = true").fetchone()[0]
    revised_target_matches = con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}' WHERE is_target_revised = true").fetchone()[0]
    
    records = [
        {
            "population_name": "Raw Ball-by-Ball Universe",
            "source_file": "data/raw/6af458274c1e8_data_pack/Data Pack/ball_by_ball.csv",
            "deliveries": int(n_raw),
            "matches": int(con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{raw_path}'").fetchone()[0]),
            "super_overs_included": True,
            "modeling_status": "Immutable Raw Ground Truth",
            "notes": "Original competition data pack"
        },
        {
            "population_name": "Canonical Match State Parquet",
            "source_file": "data/processed/match_state.parquet",
            "deliveries": int(n_total_parquet),
            "matches": int(con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}'").fetchone()[0]),
            "super_overs_included": True,
            "modeling_status": "Full Validated Delivery Universe",
            "notes": "Preserves all 200,999 deliveries with feature enrichment"
        },
        {
            "population_name": "Normal-Innings Modeling Universe",
            "source_file": "data/processed/match_state.parquet (innings in [1, 2])",
            "deliveries": int(n_normal),
            "matches": int(con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}' WHERE innings IN (1, 2)").fetchone()[0]),
            "super_overs_included": False,
            "modeling_status": "Primary Modeling Universe (Stages 3, 3.1, 4.0, 4.1)",
            "notes": "Innings 1 (105,727) + Innings 2 (95,234); exactly 200,961 deliveries"
        },
        {
            "population_name": "Super Over Descriptive Universe",
            "source_file": "data/processed/match_state.parquet (innings in [3, 4])",
            "deliveries": int(n_super_over),
            "matches": int(so_matches),
            "super_overs_included": True,
            "modeling_status": "Isolated Qualitative Stress-Test Only",
            "notes": "Innings 3 (25) + Innings 4 (13) across 6 matches; extreme 48.0% wicket rate"
        },
        {
            "population_name": "Second-Innings Chase Deliveries",
            "source_file": "data/processed/match_state.parquet (innings == 2)",
            "deliveries": int(chase_balls),
            "matches": int(con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}' WHERE innings = 2").fetchone()[0]),
            "super_overs_included": False,
            "modeling_status": "Chase Pressure Evaluation Subset",
            "notes": "All legal and extra balls bowled during 2nd innings run chases"
        },
        {
            "population_name": "Valid Required Run Rate Subset",
            "source_file": "data/processed/match_state.parquet (innings == 2 & RRR not null)",
            "deliveries": int(chase_rrr_balls),
            "matches": int(con.execute(f"SELECT COUNT(DISTINCT match_id) FROM '{parquet_path}' WHERE innings == 2 AND required_run_rate_before IS NOT NULL").fetchone()[0]),
            "super_overs_included": False,
            "modeling_status": "Active Chase Leverage Subset",
            "notes": "Deliveries where Target and RRR are computable"
        },
        {
            "population_name": "Revised-Overs Matches Subset",
            "source_file": "data/processed/match_state.parquet (is_overs_revised = true)",
            "deliveries": int(con.execute(f"SELECT COUNT(*) FROM '{parquet_path}' WHERE is_overs_revised = true").fetchone()[0]),
            "matches": int(revised_overs_matches),
            "super_overs_included": False,
            "modeling_status": "Rain/Shortened Match Context",
            "notes": "34 rain-affected matches with shortened scheduled overs"
        },
        {
            "population_name": "Revised-Target Matches Subset",
            "source_file": "data/processed/match_state.parquet (is_target_revised = true)",
            "deliveries": int(con.execute(f"SELECT COUNT(*) FROM '{parquet_path}' WHERE is_target_revised = true").fetchone()[0]),
            "matches": int(revised_target_matches),
            "super_overs_included": False,
            "modeling_status": "DLS / VJD Target Adjustment Context",
            "notes": "23 matches where target was adjusted"
        }
    ]
    
    df_reconciliation = pd.DataFrame(records)
    print("=== POPULATION_RECONCILIATION_CSV_START ===")
    print(df_reconciliation.to_csv(index=False))
    print("=== POPULATION_RECONCILIATION_CSV_END ===")
    
    return df_reconciliation


if __name__ == "__main__":
    run_population_reconciliation(Path("D:/PinkOps"))
