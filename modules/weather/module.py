from flask import Blueprint, jsonify
import requests
from system.module.module_manager import hookimpl

class WeatherModule:
    def __init__(self):
        self.blueprint = Blueprint('weather_bp', __name__)
        self.setup_routes()
        self.api_key = "your_openweathermap_api_key"  # Move to config later

    def setup_routes(self):
        @self.blueprint.route("/")  # Add root route
        def weather_home():
            """Weather module home page"""
            return jsonify({
                "message": "Welcome to Weather Module",
                "endpoints": {
                    "current": "/weather/current/<city>",
                    "forecast": "/weather/forecast/<city>"
                }
            })

        @self.blueprint.route("/current/<city>")
        def get_weather(city):
            """Get current weather for a city"""
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200:
                    weather = {
                        'city': city,
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'humidity': data['main']['humidity']
                    }
                    return jsonify(weather)
                else:
                    return jsonify({'error': 'City not found'}), 404
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.blueprint.route("/forecast/<city>")
        def get_forecast(city):
            """Get 5-day forecast for a city"""
            try:
                url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric"
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200:
                    forecast = {
                        'city': city,
                        'forecast': data['list'][:5]  # Get next 5 forecasts
                    }
                    return jsonify(forecast)
                else:
                    return jsonify({'error': 'City not found'}), 404
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    @hookimpl
    def get_routes(self):
        return [(self.blueprint, "/weather")]  # This maps /weather/* to the blueprint

    @hookimpl
    def get_manifest(self):
        return {
            'name': 'Weather',
            'version': '1.0.0',
            'main_route': '/weather',
            'icon_class': 'fa-solid fa-cloud-sun-rain',
            'type': 'app'  # Weather is a standalone app
        }

    