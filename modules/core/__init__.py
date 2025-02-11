# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Core module initialization and route registration. Sets up the core
#     functionality including authentication, user management, and system
#     settings blueprints.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint, Flask
import logging
from flask_login import current_user

from .controllers.api_routes import blueprint as api_blueprint
from .controllers.routes import blueprint as core_blueprint
from .module import CoreModule

# Create module instance
module_instance = CoreModule()

# Register routes
module_instance.register_blueprint(core_blueprint, url_prefix="")
module_instance.register_blueprint(api_blueprint, url_prefix="/api")