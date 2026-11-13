import duckdb

con = duckdb.connect()
df = con.execute("SELECT DISTINCT pace_or_spin, COUNT(*) FROM 'data/processed/match_state.parquet' GROUP BY pace_or_spin").df()
print("pace_or_spin unique values:\n", df)
