import duckdb

con = duckdb.connect()
sample_extras = con.execute("""
    SELECT extras_type, runs, extras1_runs, extras_2_runs, runs_on_delivery, COUNT(*) as cnt
    FROM 'data/processed/match_state.parquet'
    WHERE extras_type IS NOT NULL
    GROUP BY extras_type, runs, extras1_runs, extras_2_runs, runs_on_delivery
    ORDER BY extras_type, cnt DESC
""").df()
print("Sample extras breakdown in match_state.parquet:\n", sample_extras.head(25))

# Check how runs_conceded is defined or should be defined
# Batter runs: runs (runs off bat)
# Bowler runs conceded: runs + wides + noballs / overstep
bowler_runs_check = con.execute("""
    SELECT 
        extras_type,
        AVG(runs) as avg_bat_runs,
        AVG(extras1_runs) as avg_ext1,
        AVG(runs_on_delivery) as avg_total_delivery_runs
    FROM 'data/processed/match_state.parquet'
    GROUP BY extras_type
""").df()
print("\nBowler runs check by extras_type:\n", bowler_runs_check)
