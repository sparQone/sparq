# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather module initialization and route registration. Sets up weather
#     functionality including current conditions and forecast features.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import logging

# Configure module-specific logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set loggers for submodules to INFO level
logging.getLogger('modules.weather.models.weather').setLevel(logging.INFO)
logging.getLogger('modules.weather.controllers.routes').setLevel(logging.INFO)

from .controllers.routes import blueprint as weather_blueprint
from .module import WeatherModule

# Create module instance
module_instance = WeatherModule()

# Register routes
module_instance.register_blueprint(weather_blueprint, url_prefix="/weather")
