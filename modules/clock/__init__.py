# This file can be empty or contain clock module initialization logic

from flask import Blueprint
from .controllers.clock import blueprint as clock_blueprint
from .module import ClockModule

# Create module instance
module_instance = ClockModule()

# Register routes
module_instance.register_blueprint(clock_blueprint, url_prefix='/clock')
