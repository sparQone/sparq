# This file can be empty or contain tasks module initialization logic
from flask import Blueprint
from .controllers.routes import blueprint as tasks_blueprint
from .module import TasksModule

# Create module instance
module_instance = TasksModule()

# Export only the module instance
__all__ = ['module_instance']
