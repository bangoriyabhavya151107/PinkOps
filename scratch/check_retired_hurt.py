import duckdb

con = duckdb.connect()
df = con.execute("SELECT match_id, innings, striker_name, dismissal_type_raw, dismissal_type_cleaned, is_retired_hurt, is_team_wicket, is_bowler_wicket FROM 'data/processed/match_state.parquet' WHERE is_retired_hurt = 1").df()
print(df[['striker_name', 'dismissal_type_raw', 'dismissal_type_cleaned', 'is_team_wicket', 'is_bowler_wicket']])
