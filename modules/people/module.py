from flask import Blueprint
from system.module.module_manager import hookimpl
from .hooks import PeopleHookSpecs

class PeopleModule:
    def __init__(self):
        self.blueprint = Blueprint('people_bp', __name__,
                                 template_folder='views/templates',
                                 static_folder='views/assets')
        
    def register_specs(self, plugin_manager):
        """Register hook specifications with the plugin manager"""
        plugin_manager.add_hookspecs(PeopleHookSpecs)

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    @hookimpl
    def get_routes(self):
        """Get module routes"""
        return [(self._blueprint, self._url_prefix)] 