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

from .controllers.api_routes import blueprint as api_blueprint
from .controllers.routes import blueprint as core_blueprint
from .module import CoreModule

# Create module instance
module_instance = CoreModule()

# Register routes
module_instance.register_blueprint(core_blueprint, url_prefix="")
module_instance.register_blueprint(api_blueprint, url_prefix="/api")

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    # Log handler to show debug messages in console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # ... rest of your app initialization code ...
