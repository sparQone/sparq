from flask import Blueprint, current_app
from system.module.module_manager import hookimpl
from .hooks import PeopleHookSpecs
from system.db.database import db

class PeopleModule:
    def __init__(self):
        self.blueprint = Blueprint('people_bp', __name__,
                                 template_folder='views/templates',
                                 static_folder='views/assets')

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    def get_routes(self):
        """Get routes for the module"""
        from .controllers.routes import blueprint
        return [(blueprint, '/people')]

    @hookimpl
    def init_database(self):
        """Initialize database tables"""
        from .models.employee import Employee
        db.create_all()  # This will create only tables that haven't been created yet

    def register_specs(self, plugin_manager):
        """Register hook specifications and implementations"""
        plugin_manager.add_hookspecs(PeopleHookSpecs)
        plugin_manager.register(self)

# Create module instance
module_instance = PeopleModule() 