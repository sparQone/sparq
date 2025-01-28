from system.db.database import db
from system.module.module_manager import hookimpl

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
        return [(self._blueprint, self._url_prefix)]

    @hookimpl
    def init_database(self):
        """Initialize database tables"""
        from .models.task import Task
        db.create_all()  # This will create only tables that haven't been created yet

