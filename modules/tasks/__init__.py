# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Tasks module initialization and route registration. Sets up tasks
#     functionality including task management.
#
# Copyright (c) 2025 remarQable LLC

from flask import Blueprint
from .controllers.routes import blueprint as tasks_blueprint
from .module import TasksModule

# Create module instance
module_instance = TasksModule()

# Export only the module instance
__all__ = ['module_instance']
