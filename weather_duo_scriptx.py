import requests
import datetime
import pandas as pd
import time

# API Keys
openweather_api_key = "b13189c29a02211e832a5e6dfea3fbe0"
visualcrossing_api_key = "PAJRYYV7SAX8TPNHWMDD6DSR6"

# Locations (City Names)
locations = ["Orlando,FL", "Las Vegas,NV"]

# Number of past days to fetch
days_to_fetch = 15  

# File Paths
historical_file_path = "historical_weather_data.csv"
forecast_file_path = "forecast_weather_data.csv"
current_weather_file_path = "current_weather_data.csv"

# Lists to store data
historical_records = []
forecast_records = []
current_records = []

# OpenWeather API URLs
current_weather_url = "http://api.openweathermap.org/data/2.5/weather"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
visualcrossing_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

# Function to Fetch Data with Retry Mechanism
def fetch_weather_data(url, retries=3, params=None):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API error: {e} (Attempt {attempt + 1} of {retries})")
            time.sleep(2)
    return None

# 📌 Fetch Historical Data from Visual Crossing (Batch Request)
for city in locations:
    print(f"\nFetching historical weather for {city}...")

    url = f"{visualcrossing_url}{city}/last{days_to_fetch}days?key={visualcrossing_api_key}&unitGroup=us"

    data = fetch_weather_data(url)

    if data and "days" in data:
        for weather in data["days"]:
            date = weather["datetime"]
            temp_f = weather.get("temp", 0)
            temp_max_f = weather.get("tempmax", 0)
            temp_min_f = weather.get("tempmin", 0)
            humidity = weather.get("humidity", 0)
            wind_speed = weather.get("windspeed", 0)
            precipitation = weather.get("precip", 0)
            description = weather.get("conditions", "No description")

            historical_records.append([city, date, temp_f, temp_max_f, temp_min_f, humidity, wind_speed, precipitation, description])

        print(f"✅ Historical data retrieved for {city}.")

    else:
        print(f"❌ Skipping {city} due to missing data.")

    time.sleep(5)  # Increase delay to avoid rate limits

# Save Historical Data to CSV
df_historical = pd.DataFrame(historical_records, columns=['City', 'Date', 'Temp (F)', 'Temp Max (F)', 'Temp Min (F)', 'Humidity', 'Wind Speed', 'Precipitation', 'Description'])
df_historical.to_csv(historical_file_path, index=False)
print(f"\n📂 Historical weather data saved to {historical_file_path}")
