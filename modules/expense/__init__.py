from flask import Blueprint
from .controllers.routes import blueprint as expense_blueprint
from .module import ExpenseModule

# Create module instance
module_instance = ExpenseModule()

# Register routes
module_instance.register_blueprint(expense_blueprint, url_prefix='/expense') 