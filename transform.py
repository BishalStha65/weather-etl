import pandas as pd
from datetime import datetime, timezone

def transform_weather_data(raw_data_list):
    records = []

    for data in raw_data_list:
        record = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature_celsius": round(data["main"]["temp"] - 273.15, 2),  # Convert from Kelvin to Celsius
            "feels_like_celsius": round(data["main"]["feels_like"] - 273.15, 2),  # Convert from Kelvin to Celsius
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather_description": data["weather"][0]["description"],
            "data_timestamp": datetime.fromtimestamp(data["dt"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "pipeline_run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),

        }
        records.append(record)

    df = pd.DataFrame(records)

    df = df.fillna({"weather_description": "unkown", "wind_speed": 0.0})

    df["temperature_celsius"] = df["temperature_celsius"].astype(float)
    df["feels_like_celsius"] = df["feels_like_celsius"].astype(float)
    df["humidity"] = df["humidity"].astype(int)
    df["pressure"] = df["pressure"].astype(int)
    df["wind_speed"] = df["wind_speed"].astype(float)

    return df

if __name__ == "__main__":
    from extract import extract_all_cities
    from config import API_KEY, CITIES

    print("Testing transformation...")
    raw_data = extract_all_cities(CITIES, API_KEY)
    df = transform_weather_data(raw_data)
    print(df)
    print(f"\nShape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")

