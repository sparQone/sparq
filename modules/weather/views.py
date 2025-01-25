from flask import Blueprint, jsonify

weather_bp = Blueprint('weather_bp', __name__)

@weather_bp.route('/current')
def current_weather():
    """
    Returns fake weather data for Minneapolis.
    """
    # Just returning a static JSON for now
    fake_data = {
        "city": "Minneapolis",
        "temperature": "25°F",
        "condition": "Snowy",
        "forecast": "Light snow showers possible."
    }
    return jsonify(fake_data)

def init_module(app):
    """
    The loader function that registers this module's blueprint.
    Called automatically by our scanning logic in app.py.
    """
    app.register_blueprint(weather_bp, url_prefix='/weather')
    print("Weather module initialized.")
