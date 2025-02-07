# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module initialization and route registration. Sets up HR and
#     employee management functionality including profiles and scheduling.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from .module import PeopleModule
from .utils.filters import init_filters

# Create module instance
module_instance = PeopleModule()

def init_module(app):
    """Initialize the people module"""
    # Initialize filters first
    init_filters(app)
    
    # Import and register blueprint with routes
    from .controllers import blueprint
    app.register_blueprint(blueprint, url_prefix='/people') 