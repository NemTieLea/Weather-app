import requests
import json
from datetime import datetime, timedelta
import os

CACHE_FILE = "weather_cache.json"


def read_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}


def write_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)


def get_weather(date):
    latitude = 52.2297
    longitude = 21.0122
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation",
        "daily": "precipitation_sum",
        "timezone": "Europe/Warsaw",
        "start_date": date,
        "end_date": date
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            precipitation_sum = data['daily']['precipitation_sum'][0]
            return precipitation_sum
        except (KeyError, IndexError):
            return None
    else:
        return None


def check_rain():
    user_date = input("Enter date (YYYY-mm-dd) or leave blank to see the next day: ")
    if not user_date:
        user_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    cache = read_cache()

    if user_date in cache:
        precipitation_sum = cache[user_date]
    else:
        precipitation_sum = get_weather(user_date)
        if precipitation_sum is not None:
            cache[user_date] = precipitation_sum
            write_cache(cache)

    if precipitation_sum is None:
        print("I don't know.")
    elif precipitation_sum > 0.0:
        print("It will rain.")
    else:
        print("It will not rain.")


if __name__ == "__main__":
    check_rain()
