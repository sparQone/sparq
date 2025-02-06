# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Appointments module class that implements scheduling and calendar
#     management. Handles route registration and database initialization
#     for the appointment booking system.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------
from flask import Blueprint, current_app
from system.module.hooks import hookimpl
from system.db.database import db

class AppointmentsModule:
    def __init__(self):
        self.blueprint = Blueprint('appointments_bp', __name__,
                                 template_folder='views/templates',
                                 static_folder='views/assets')
        
    def register_blueprint(self, blueprint, url_prefix):
        self._blueprint = blueprint
        self._url_prefix = url_prefix
        
    def get_routes(self):
        return [(self._blueprint, self._url_prefix)]
