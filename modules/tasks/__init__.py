# This file can be empty or contain tasks module initialization logic
from flask import Blueprint
from .controllers.routes import blueprint as tasks_blueprint
from .module import TasksModule

# Create module instance
module_instance = TasksModule()

# Register routes
module_instance.register_blueprint(tasks_blueprint, url_prefix='/tasks')
