from pluggy import HookimplMarker

hookimpl = HookimplMarker("sparqone")

class CoreModule:
    """Core module providing basic functionality"""
    
    @hookimpl
    def get_routes(self):
        """Get module routes"""
        from .controllers.routes import blueprint
        return [(blueprint, '')]

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix 