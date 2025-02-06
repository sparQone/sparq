# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Clock module class that implements clock functionality.
#     Handles route registration and blueprint registration.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint, current_app

class ClockModule:
    def __init__(self):
        self.blueprint = Blueprint('clock_bp', __name__,
                                 template_folder='views/templates',
                                 static_folder='views/assets')
        
    def register_blueprint(self, blueprint, url_prefix):
        self._blueprint = blueprint
        self._url_prefix = url_prefix
        
    def get_routes(self):
        return [(self._blueprint, self._url_prefix)] 