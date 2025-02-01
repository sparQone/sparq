# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Core module class that implements the plugin system hooks and handles
#     route registration for the core functionality. Provides essential
#     application features and module management.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from pluggy import HookimplMarker
from flask import Blueprint
from system.module.hooks import hookimpl  # Updated import

class CoreModule:
    """Core module providing basic functionality"""
    
    @hookimpl
    def get_routes(self):
        """Get module routes"""
        from .controllers.routes import blueprint
        return [(blueprint, '')]

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix 