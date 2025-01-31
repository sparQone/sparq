# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Appointments module initialization and route registration. Sets up
#     scheduling and calendar management functionality including booking
#     and availability management.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from .controllers.routes import blueprint as appointments_blueprint
from .module import AppointmentsModule

# Create module instance
module_instance = AppointmentsModule()

# Register routes
module_instance.register_blueprint(appointments_blueprint, url_prefix='/appointments') 