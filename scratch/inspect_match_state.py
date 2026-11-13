import duckdb

con = duckdb.connect()
raw_csv = "data/raw/6af458274c1e8_data_pack/Data Pack/ball_by_ball.csv"

raw_count = con.execute(f"SELECT COUNT(*) FROM '{raw_csv}'").fetchone()[0]
print("Raw ball_by_ball.csv row count:", raw_count)

parquet_count = con.execute("SELECT COUNT(*) FROM 'data/processed/match_state.parquet'").fetchone()[0]
print("match_state.parquet row count:", parquet_count)

inn_df = con.execute("SELECT innings, COUNT(*) as balls FROM 'data/processed/match_state.parquet' GROUP BY innings ORDER BY innings").df()
print("\nInnings breakdown in match_state.parquet:\n", inn_df)

raw_sample = con.execute(f"SELECT * FROM '{raw_csv}' LIMIT 3").df()
print("\nRaw ball_by_ball.csv columns:")
for col in raw_sample.columns:
    print(f"  {col} ({raw_sample[col].dtype})")

dismissal_kinds_raw = con.execute(f"""
    SELECT dismissal_type, COUNT(*) as cnt 
    FROM '{raw_csv}' 
    WHERE dismissal_type IS NOT NULL AND dismissal_type != '' 
    GROUP BY dismissal_type 
    ORDER BY cnt DESC
""").df()
print("\nDismissal types in raw ball_by_ball.csv:\n", dismissal_kinds_raw)

dismissal_kinds_parquet = con.execute("""
    SELECT dismissal_type_cleaned, is_bowler_wicket, is_team_wicket, is_retired_hurt, COUNT(*) as cnt 
    FROM 'data/processed/match_state.parquet' 
    WHERE dismissal_type_cleaned IS NOT NULL 
    GROUP BY dismissal_type_cleaned, is_bowler_wicket, is_team_wicket, is_retired_hurt 
    ORDER BY cnt DESC
""").df()
print("\nDismissal types in match_state.parquet:\n", dismissal_kinds_parquet)

extras_types_raw = con.execute(f"""
    SELECT extras_type, COUNT(*) as cnt 
    FROM '{raw_csv}' 
    WHERE extras_type IS NOT NULL AND extras_type != '' 
    GROUP BY extras_type 
    ORDER BY cnt DESC
""").df()
print("\nExtras types in raw ball_by_ball.csv:\n", extras_types_raw)
