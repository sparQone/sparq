# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather model that handles weather data retrieval and caching.
#     Implements integration with external weather service APIs and
#     provides weather information formatting.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import requests


class Weather:
    # Weather code mappings
    WEATHER_CODES = {
        0: {"description": "Clear sky", "icon": "01d"},
        1: {"description": "Mainly clear", "icon": "02d"},
        2: {"description": "Partly cloudy", "icon": "03d"},
        3: {"description": "Overcast", "icon": "04d"},
        45: {"description": "Foggy", "icon": "50d"},
        48: {"description": "Depositing rime fog", "icon": "50d"},
        51: {"description": "Light drizzle", "icon": "09d"},
        53: {"description": "Moderate drizzle", "icon": "09d"},
        55: {"description": "Dense drizzle", "icon": "09d"},
        61: {"description": "Slight rain", "icon": "10d"},
        63: {"description": "Moderate rain", "icon": "10d"},
        65: {"description": "Heavy rain", "icon": "10d"},
        71: {"description": "Slight snow fall", "icon": "13d"},
        73: {"description": "Moderate snow fall", "icon": "13d"},
        75: {"description": "Heavy snow fall", "icon": "13d"},
        77: {"description": "Snow grains", "icon": "13d"},
        80: {"description": "Slight rain showers", "icon": "09d"},
        81: {"description": "Moderate rain showers", "icon": "09d"},
        82: {"description": "Violent rain showers", "icon": "09d"},
        85: {"description": "Slight snow showers", "icon": "13d"},
        86: {"description": "Heavy snow showers", "icon": "13d"},
        95: {"description": "Thunderstorm", "icon": "11d"},
        96: {"description": "Thunderstorm with slight hail", "icon": "11d"},
        99: {"description": "Thunderstorm with heavy hail", "icon": "11d"},
    }

    def get_current_weather(self, city):
        """Get current weather for a city"""
        try:
            # First get coordinates for the city
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_response = requests.get(geocoding_url)
            geo_data = geo_response.json()

            if not geo_data.get("results"):
                raise ValueError("City not found")

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]

            # Then get weather for those coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&temperature_unit=fahrenheit"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if "error" in weather_data:
                raise ValueError(weather_data["reason"])

            return weather_data

        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch weather data: {str(e)}")

    def get_weather_description(self, code):
        """Get weather description from code"""
        return self.WEATHER_CODES.get(code, {"description": "Unknown"})["description"]

    def get_weather_icon(self, code):
        """Get weather icon from code"""
        return self.WEATHER_CODES.get(code, {"icon": "03d"})["icon"]
