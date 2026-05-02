import duckdb
from config import DB_PATH


def run_queries():
    """Run analytical SQL queries on the weather data."""
    con = duckdb.connect(DB_PATH)

    # Query 1: All data for a specific city
    print("=" * 50)
    print("Query 1: All weather data for London")
    print("=" * 50)
    result = con.execute("""
        SELECT city, temperature_celsius, humidity, weather_description, data_timestamp
        FROM weather_data
        WHERE city = 'London'
        ORDER BY data_timestamp DESC
    """).fetchdf()
    print(result)

    # Query 2: Average temperature per city
    print("\n" + "=" * 50)
    print("Query 2: Average temperature per city")
    print("=" * 50)
    result = con.execute("""
        SELECT
            city,
            ROUND(AVG(temperature_celsius), 2) AS avg_temp,
            ROUND(MIN(temperature_celsius), 2) AS min_temp,
            ROUND(MAX(temperature_celsius), 2) AS max_temp,
            COUNT(*) AS readings
        FROM weather_data
        GROUP BY city
        ORDER BY avg_temp DESC
    """).fetchdf()
    print(result)

    # Query 3: Hottest and coldest cities
    print("\n" + "=" * 50)
    print("Query 3: Current hottest and coldest cities")
    print("=" * 50)
    result = con.execute("""
        SELECT city, temperature_celsius, humidity, weather_description
        FROM weather_data
        WHERE data_timestamp = (
            SELECT MAX(data_timestamp) FROM weather_data
        )
        ORDER BY temperature_celsius DESC
    """).fetchdf()
    print(result)

    # Query 4: Temperature change using LAG window function
    print("\n" + "=" * 50)
    print("Query 4: Temperature change between readings (LAG)")
    print("=" * 50)
    result = con.execute("""
        SELECT
            city,
            data_timestamp,
            temperature_celsius,
            LAG(temperature_celsius) OVER (
                PARTITION BY city ORDER BY data_timestamp
            ) AS previous_temp,
            ROUND(
                temperature_celsius - LAG(temperature_celsius) OVER (
                    PARTITION BY city ORDER BY data_timestamp
                ), 2
            ) AS temp_change
        FROM weather_data
        ORDER BY city, data_timestamp
    """).fetchdf()
    print(result)


    # Query 5: Export to CSV
    print("\n" + "=" * 50)
    print("Query 5: Exporting average temps to CSV...")
    print("=" * 50)
    con.execute("""
        COPY (
            SELECT
                city,
                ROUND(AVG(temperature_celsius), 2) AS avg_temp,
                ROUND(AVG(humidity), 2) AS avg_humidity,
                COUNT(*) AS total_readings
            FROM weather_data
            GROUP BY city
            ORDER BY avg_temp DESC
        ) TO 'weather_summary.csv' (HEADER, DELIMITER ',')
    """)
    print("  Exported to weather_summary.csv")

    con.close()


if __name__ == "__main__":
    run_queries()