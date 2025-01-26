from pluggy import HookimplMarker

hookimpl = HookimplMarker("sparqone")

class CoreModule:
    """Core module providing basic functionality"""
    
    @hookimpl
    def get_routes(self):
        """Get module routes"""
        from .controllers.core import blueprint
        return [(blueprint, '')]

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    def icon_class_filter(self, module_name):
        """Get icon class for a module"""
        from flask import current_app
        modules = current_app.config.get('INSTALLED_MODULES', [])
        for module in modules:
            if module['name'].lower() == module_name.lower():
                return module.get('icon_class', 'fa-solid fa-puzzle-piece')
        return 'fa-solid fa-puzzle-piece' 