# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Clock module initialization and route registration. Sets up clock
#     functionality including time tracking and reporting.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint

from .controllers.routes import blueprint as clock_blueprint
from .module import ClockModule

# Create module instance
module_instance = ClockModule()

# Register routes
module_instance.register_blueprint(clock_blueprint, url_prefix="/clock")
