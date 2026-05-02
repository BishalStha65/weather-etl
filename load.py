import duckdb
from config import DB_PATH


def load_to_duckdb(df, db_path):
    """Load transformed DataFrame into DuckDB database."""
    con = duckdb.connect(db_path)

    # Create table if it does not exist
    con.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            city VARCHAR,
            country VARCHAR,
            temperature_celsius DOUBLE,
            feels_like_celsius DOUBLE,
            humidity INTEGER,
            pressure INTEGER,
            wind_speed DOUBLE,
            weather_description VARCHAR,
            data_timestamp VARCHAR,
            pipeline_run_date VARCHAR
        )
    """)

    # Check for duplicates before inserting
    existing = con.execute(
        "SELECT city, data_timestamp FROM weather_data"
    ).fetchdf()

    if not existing.empty:
        # Filter out rows that already exist
        merged = df.merge(
            existing, on=["city", "data_timestamp"], how="left", indicator=True
        )
        new_rows = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
    else:
        new_rows = df

    if not new_rows.empty:
        con.execute("INSERT INTO weather_data SELECT * FROM new_rows")
        print(f"  Loaded {len(new_rows)} new rows into weather_data")
    else:
        print("  No new rows to load (all duplicates)")

    con.close()


if __name__ == "__main__":
    from extract import extract_all_cities
    from transform import transform_weather_data
    from config import API_KEY, CITIES, DB_PATH

    print("Testing load...")
    raw_data = extract_all_cities(CITIES, API_KEY)
    df = transform_weather_data(raw_data)
    load_to_duckdb(df, DB_PATH)

    # Verify the data
    con = duckdb.connect(DB_PATH)
    result = con.execute("SELECT * FROM weather_data").fetchdf()
    print(f"\nRows in database: {len(result)}")
    print(result)
    con.close()