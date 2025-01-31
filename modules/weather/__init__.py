# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather module initialization and route registration. Sets up weather
#     functionality including current conditions and forecast features.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from .controllers.routes import blueprint as weather_blueprint
from .module import WeatherModule

# Create module instance
module_instance = WeatherModule()

# Register routes
module_instance.register_blueprint(weather_blueprint, url_prefix='/weather')
