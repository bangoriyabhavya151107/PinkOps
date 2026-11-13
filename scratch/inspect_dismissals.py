import duckdb

con = duckdb.connect()
ro_df = con.execute("""
    SELECT 
        dismissal_type_cleaned,
        COUNT(*) as total_dismissals,
        SUM(CASE WHEN dismissed_player_id_cleaned = striker_id THEN 1 ELSE 0 END) as striker_dismissed,
        SUM(CASE WHEN dismissed_player_id_cleaned = non_striker_id THEN 1 ELSE 0 END) as non_striker_dismissed,
        SUM(CASE WHEN dismissed_player_id_cleaned NOT IN (striker_id, non_striker_id) THEN 1 ELSE 0 END) as neither_dismissed
    FROM 'data/processed/match_state.parquet'
    WHERE dismissal_type_cleaned IS NOT NULL
    GROUP BY dismissal_type_cleaned
    ORDER BY total_dismissals DESC
""").df()
print("Dismissal attribution striker vs non-striker:\n", ro_df)
