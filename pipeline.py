from extract import extract_all_cities
from transform import transform_weather_data
from load import load_to_duckdb
from config import API_KEY, CITIES, DB_PATH
import duckdb


def run_pipeline():
    """Run the full ETL pipeline."""
    print("=" * 50)
    print("WEATHER DATA ETL PIPELINE")
    print("=" * 50)

    # Step 1: Extract
    print("\n[1/3] Extracting weather data...")
    raw_data = extract_all_cities(CITIES, API_KEY)
    print(f"  Extracted data for {len(raw_data)} cities")

    # Step 2: Transform
    print("\n[2/3] Transforming data...")
    df = transform_weather_data(raw_data)
    print(f"  Transformed {len(df)} records")
    print(f"  Columns: {list(df.columns)}")

    # Step 3: Load
    print("\n[3/3] Loading data into DuckDB...")
    load_to_duckdb(df, DB_PATH)

    # Summary
    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE")
    con = duckdb.connect(DB_PATH)
    count = con.execute("SELECT COUNT(*) FROM weather_data").fetchone()[0]
    print(f"Total rows in database: {count}")
    con.close()
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()