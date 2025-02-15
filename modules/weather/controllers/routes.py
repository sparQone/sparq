# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather module route handlers for displaying weather information and
#     handling weather data lookups via external API integration.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from flask_login import login_required

from ..models.weather import Weather

# Create blueprint
blueprint = Blueprint(
    "weather_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)

# Initialize weather
weather = Weather()


@blueprint.route("/")
@login_required
def weather_home():
    """Weather module home page"""
    return render_template(
        "weather/index.html", title="Weather", module_home="weather_bp.weather_home"
    )


@blueprint.route("/lookup", methods=["POST"])
def lookup_weather():
    """AJAX endpoint for weather lookup"""
    try:
        city = request.json.get("city")
        if not city:
            return jsonify({"error": "City is required"}), 400

        weather_data = weather.get_current_weather(city)

        # Format the response
        response = {
            "temperature": weather_data["current"]["temperature_2m"],
            "humidity": weather_data["current"]["relative_humidity_2m"],
            "description": weather.get_weather_description(weather_data["current"]["weather_code"]),
            "icon": weather.get_weather_icon(weather_data["current"]["weather_code"]),
        }

        return jsonify(response)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Failed to fetch weather data"}), 500
