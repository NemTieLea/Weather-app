import requests
import json
from datetime import datetime, timedelta
import os

CACHE_FILE = "weather_cache.json"


class WeatherForecast:
    def __init__(self, cache_file=CACHE_FILE):
        self.cache_file = cache_file
        self.cache = self.read_cache()

    def read_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                return json.load(file)
        return {}

    def write_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)

    def get_weather(self, date):
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

    def __setitem__(self, date, value):
        self.cache[date] = value
        self.write_cache()

    def __getitem__(self, date):
        if date in self.cache:
            return self.cache[date]
        else:
            precipitation_sum = self.get_weather(date)
            if precipitation_sum is not None:
                self.cache[date] = precipitation_sum
                self.write_cache()
                return precipitation_sum
            else:
                return None

    def __iter__(self):
        return iter(self.cache.keys())

    def items(self):
        return ((date, weather) for date, weather in self.cache.items())


def check_rain():
    weather_forecast = WeatherForecast()

    user_date = input("Enter date (YYYY-mm-dd) or leave blank to see the next day: ")
    if not user_date:
        user_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    rain_sum = weather_forecast[user_date]

    if rain_sum is None:
        print("I don't know.")
    elif rain_sum > 0.0:
        print("It will rain.")
    else:
        print("It will not rain.")


if __name__ == "__main__":
    check_rain()
