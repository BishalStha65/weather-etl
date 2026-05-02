import requests
from config import API_KEY, CITIES

def extract_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    # send city name & API Key as query paramters
    params = {
        "q": city,
        "appid": api_key,
    }

    response =requests.get(url, params=params)

    if response.status_code == 200:
        print(f"Successfully extracted weather data for {city}")
        return response.json()
    else:
        print(f"Failed to extract weather data for {city}. Status code: {response.status_code}")
        return None
    
def extract_all_cities(cities, api_key):
    raw_data = []
    for city in cities:
        data = extract_weather(city, api_key)
        if data is not None:
            raw_data.append(data)
    return raw_data

if __name__ == "__main__":
    import json

    print("Testing extraction for London...")
    result = extract_weather("London", API_KEY)
    if result:
        print(json.dumps(result, indent=2))