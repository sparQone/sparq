#
# Description:
#     E-Sign module initialization and route registration. Sets up e-sign
#     functionality including e-signing and document management.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------
from flask import Blueprint
from .controllers.routes import blueprint as esign_blueprint

# Create module instance
module_instance = ESignModule()

# Register routes
module_instance.register_blueprint(esign_blueprint, url_prefix='/esign') 