# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Tasks module class that implements task management functionality.
#     Handles module registration and blueprint registration.
#
# Copyright (c) 2025 remarQable LLC

from system.db.database import db
from system.module.hooks import hookimpl


class TasksModule:
    def __init__(self):
        """Initialize module"""
        self._blueprint = None
        self._url_prefix = None

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    def get_routes(self):
        """Get module routes"""
        from .controllers.routes import blueprint as tasks_blueprint

        return [(tasks_blueprint, "/tasks")]

    @hookimpl
    def init_database(self):
        """Initialize database tables and sample data"""
        from .models.task import Task

        db.create_all()
        try:
            Task.create_sample_data()
        except Exception as e:
            print(f"Error creating sample tasks: {e}")
