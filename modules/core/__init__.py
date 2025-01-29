# This file can be empty or contain core module initialization logic

from flask import Blueprint
from .module import CoreModule
from .controllers.core import blueprint as core_blueprint

# Create module instance
module_instance = CoreModule()

# Register routes
module_instance.register_blueprint(core_blueprint, url_prefix='')
