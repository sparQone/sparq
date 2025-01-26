from flask import Blueprint
from .controllers.books import blueprint as books_blueprint
from .module import BooksModule

# Create module instance
module_instance = BooksModule()

# Register routes
module_instance.register_blueprint(books_blueprint, url_prefix='/books') 