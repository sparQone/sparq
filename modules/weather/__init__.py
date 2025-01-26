# This file can be empty or contain weather module initialization logic

from flask import Blueprint
from .controllers.weather import blueprint as weather_blueprint
from .module import WeatherModule

# Create module instance
module_instance = WeatherModule()

# Register routes
module_instance.register_blueprint(weather_blueprint, url_prefix='/weather')
