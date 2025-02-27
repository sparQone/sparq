# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather module routes. Handles weather data retrieval and display.
#     Implements integration with external weather service APIs and
#     provides weather information formatting.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import logging
import traceback
from flask import Blueprint, render_template, request, jsonify, flash, current_app
from flask_login import login_required
from modules.weather.models.weather import Weather

# Create blueprint
blueprint = Blueprint(
    "weather_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)

# Initialize weather service
weather_service = Weather()

# Set up logger
logger = logging.getLogger(__name__)


@blueprint.route("/", methods=["GET"])
@login_required
def weather_home():
    """Render the weather module home page"""
    logger.info("Rendering weather home page")
    return render_template("weather/index.html", title="Weather", module_home="weather_bp.weather_home")


@blueprint.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup_weather():
    """Handle weather lookup requests"""
    # Get city from form data or query parameters
    if request.method == "POST":
        city = request.form.get("city")
    else:  # GET request
        city = request.args.get("city")
    
    logger.info(f"Weather lookup requested for city: {city}")
    
    if not city:
        logger.warning("Weather lookup attempted with empty city name")
        return render_weather_error("Please enter a city name")
    
    try:
        # Get weather data
        logger.info(f"Fetching weather data for {city}")
        
        try:
            weather_data = weather_service.get_current_weather(city)
        except Exception as e:
            logger.exception(f"Exception in get_current_weather: {str(e)}")
            return render_weather_error(f"Error fetching weather data: {str(e)}")
        
        # Extract current weather
        current = weather_data.get("current", {})
        if not current:
            logger.error(f"No current weather data found in response for {city}")
            return render_weather_error(f"Could not retrieve weather data for {city}")
        
        # Get weather code and description
        weather_code = current.get("weather_code")
        
        description = weather_service.get_weather_description(weather_code)
        icon = weather_service.get_weather_icon(weather_code)
        
        # Format response data
        weather_info = {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "description": description,
            "icon": icon
        }
        
        logger.info(f"Weather data retrieved successfully for {city}")
        
        # Render weather data partial
        return render_weather_data(city, weather_info)
        
    except ValueError as e:
        logger.error(f"Value error in weather lookup for {city}: {str(e)}")
        return render_weather_error(str(e))
    except Exception as e:
        logger.exception(f"Unexpected error in weather lookup for {city}")
        return render_weather_error(f"An unexpected error occurred: {str(e)}")


def render_weather_data(city, weather_info):
    """Render weather data partial"""
    # Get icon class based on icon code
    icon_map = {
        '01d': 'sun',                    # Clear sky (code 0)
        '02d': 'cloud-sun',              # Mainly clear (code 1)
        '03d': 'cloud',                  # Partly cloudy (code 2)
        '04d': 'cloud',                  # Overcast (code 3)
        '09d': 'cloud-rain',             # Drizzle (codes 51,53,55)
        '10d': 'cloud-showers-heavy',    # Rain (codes 61,63,65)
        '11d': 'bolt',                   # Thunderstorm (codes 95,96,99)
        '13d': 'snowflake',              # Snow (codes 71,73,75,77)
        '50d': 'smog',                   # Fog (codes 45,48)
        # Night variations
        '01n': 'moon',                   # Clear night
        '02n': 'cloud-moon',             # Mainly clear night
        '03n': 'cloud',                  # Partly cloudy night
        '04n': 'cloud',                  # Overcast night
        '09n': 'cloud-rain',             # Drizzle night
        '10n': 'cloud-showers-heavy',    # Rain night
        '11n': 'bolt',                   # Thunderstorm night
        '13n': 'snowflake',              # Snow night
        '50n': 'smog'                    # Fog night
    }
    
    icon_class = f"weather-icon fas fa-{icon_map.get(weather_info['icon'], 'cloud')}"
    
    # Format temperature with proper rounding
    try:
        temp = float(weather_info['temperature'])
        formatted_temp = f"{round(temp)}°F"
    except (TypeError, ValueError):
        formatted_temp = "N/A"
    
    # Format humidity
    try:
        humidity = float(weather_info['humidity'])
        formatted_humidity = f"{round(humidity)}%"
    except (TypeError, ValueError):
        formatted_humidity = "N/A"
    
    html = f"""
    <div class="text-center p-4">
        <h3 class="fs-2 fw-medium text-dark mb-3 text-capitalize">{city}</h3>
        <div class="mb-4">
            <i class="{icon_class} mb-3"></i>
            <div class="fs-1 fw-medium">{formatted_temp}</div>
        </div>
        <div class="mb-3">
            <div class="fs-4 text-secondary mb-3 text-capitalize">{weather_info['description']}</div>
            <div class="d-flex justify-content-center gap-4 text-secondary">
                <div>Humidity: <span class="fw-medium text-dark">{formatted_humidity}</span></div>
            </div>
        </div>
    </div>
    """
    
    return html


def render_weather_error(message):
    """Render weather error partial"""
    html = f"""
    <div class="d-flex flex-column align-items-center justify-content-center p-5 text-danger text-center">
        <i class="fas fa-exclamation-circle fs-1 mb-3"></i>
        <p>{message}</p>
    </div>
    """
    
    return html
