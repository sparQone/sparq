from flask import Blueprint
from .controllers.routes import blueprint as appointments_blueprint
from .module import AppointmentsModule

# Create module instance
module_instance = AppointmentsModule()

# Register routes
module_instance.register_blueprint(appointments_blueprint, url_prefix='/appointments') 