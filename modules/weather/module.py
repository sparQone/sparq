# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather module initialization and configuration. Handles blueprint
#     registration and database setup for the weather functionality.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from system.module.hooks import hookimpl
from system.db.database import db

class WeatherModule:
    def __init__(self):
        self.blueprint = Blueprint('weather_bp', __name__,
                                 template_folder='views/templates',
                                 static_folder='views/assets')

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    def get_routes(self):
        """Get routes for the module"""
        from .controllers.routes import blueprint
        return [(blueprint, '/weather')]

    @hookimpl
    def init_database(self):
        """Initialize database tables"""
        db.create_all()

# Create module instance
module_instance = WeatherModule() 