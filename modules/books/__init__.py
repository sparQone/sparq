# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Books module initialization and route registration. Sets up books
#     functionality including bookkeeping and accounting.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from .controllers.routes import blueprint as books_blueprint
from .module import BooksModule

# Create module instance
module_instance = BooksModule()

# Register routes
module_instance.register_blueprint(books_blueprint, url_prefix='/books') 