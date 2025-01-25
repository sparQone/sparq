from flask import Blueprint, render_template, jsonify, request, current_app, g
from ..models.weather import Weather
from flask_login import login_required

# Create blueprint
blueprint = Blueprint(
    'weather_bp', 
    __name__, 
    template_folder='../views/templates'
)

# Initialize weather
weather = Weather()

@blueprint.route("/")
@login_required
def weather_home():
    """Weather lookup page"""
    return render_template("weather.html",
                         module_name="Weather",
                         module_icon="fa-solid fa-cloud-sun-rain",
                         module_home='weather_bp.weather_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/lookup", methods=['POST'])
def lookup_weather():
    """AJAX endpoint for weather lookup"""
    try:
        city = request.json.get('city')
        if not city:
            return jsonify({'error': 'City is required'}), 400
            
        weather_data = weather.get_current_weather(city)
        return jsonify(weather_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 