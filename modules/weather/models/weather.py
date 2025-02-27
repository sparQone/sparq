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
import logging
import traceback
import json
import time

# Set up logger
logger = logging.getLogger(__name__)

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
            logger.info(f"Getting weather for city: {city}")
            
            # First get coordinates for the city
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            
            try:
                geo_response = requests.get(geocoding_url, timeout=10)
                
                if geo_response.status_code != 200:
                    logger.error(f"Geocoding API error: {geo_response.text}")
                    raise ValueError(f"Geocoding API error: {geo_response.status_code}")
                    
                geo_data = geo_response.json()
            except requests.exceptions.Timeout:
                logger.error("Geocoding API timeout")
                raise ValueError(f"Geocoding service timed out. Please try again later.")
            except requests.exceptions.RequestException as e:
                logger.exception(f"Request exception in geocoding: {str(e)}")
                raise ValueError(f"Failed to connect to geocoding service: {str(e)}")

            if not geo_data.get("results"):
                logger.warning(f"City not found: {city}")
                raise ValueError(f"City '{city}' not found")

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            logger.info(f"Found coordinates for {city}: lat={lat}, lon={lon}")

            # Then get weather for those coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&temperature_unit=fahrenheit"
            
            try:
                weather_response = requests.get(weather_url, timeout=10)
                
                if weather_response.status_code != 200:
                    logger.error(f"Weather API error: {weather_response.text}")
                    raise ValueError(f"Weather API error: {weather_response.status_code}")
                    
                weather_data = weather_response.json()
            except requests.exceptions.Timeout:
                logger.error("Weather API timeout")
                raise ValueError(f"Weather service timed out. Please try again later.")
            except requests.exceptions.RequestException as e:
                logger.exception(f"Request exception in weather API: {str(e)}")
                raise ValueError(f"Failed to connect to weather service: {str(e)}")

            if "error" in weather_data:
                logger.error(f"Weather API returned error: {weather_data.get('reason', 'Unknown error')}")
                raise ValueError(weather_data.get("reason", "Unknown error"))

            # Verify that we have the expected data structure
            if "current" not in weather_data:
                logger.error(f"Weather API response missing 'current' data")
                raise ValueError("Weather data format is invalid")
                
            current = weather_data.get("current", {})
            if "weather_code" not in current:
                logger.warning(f"Weather code missing in response")
                # Continue anyway, we'll use a default icon
            
            logger.info(f"Successfully retrieved weather data for {city}")
            return weather_data

        except ValueError as e:
            logger.exception(f"ValueError in get_current_weather: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in get_current_weather: {str(e)}")
            raise ValueError(f"An error occurred: {str(e)}")

    def get_weather_description(self, code):
        """Get weather description from code"""
        if code is None:
            logger.warning("Weather code is None, returning default description")
            return "Unknown"
            
        description = self.WEATHER_CODES.get(code, {"description": "Unknown"})["description"]
        return description

    def get_weather_icon(self, code):
        """Get weather icon from code"""
        if code is None:
            logger.warning("Weather code is None, returning default icon")
            return "03d"
            
        icon = self.WEATHER_CODES.get(code, {"icon": "03d"})["icon"]
        return icon
