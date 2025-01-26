from flask import Blueprint
from .controllers.esign import blueprint as esign_blueprint
from .module import ESignModule

# Create module instance
module_instance = ESignModule()

# Register routes
module_instance.register_blueprint(esign_blueprint, url_prefix='/esign') 