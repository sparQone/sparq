# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module initialization and route registration. Sets up HR and
#     employee management functionality including profiles and scheduling.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from .controllers.routes import blueprint as people_blueprint
from .module import PeopleModule

# Create module instance
module_instance = PeopleModule()

# Register routes
module_instance.register_blueprint(people_blueprint, url_prefix='/people') 