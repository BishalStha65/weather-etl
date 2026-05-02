from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
CITIES= ["London", "New York", "Tokyo", "Paris", "Sydney"]
DB_PATH= "weather.duckdb"