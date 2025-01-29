from flask import Blueprint
from .controllers.routes import blueprint as books_blueprint
from .module import BooksModule

# Create module instance
module_instance = BooksModule()

# Register routes
module_instance.register_blueprint(books_blueprint, url_prefix='/books') 