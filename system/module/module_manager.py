import pluggy

# Define hookspecs and hookimpl markers
hookspec = pluggy.HookspecMarker("sparqone")
hookimpl = pluggy.HookimplMarker("sparqone")

class ModuleSpecs:
    @hookspec
    def modify_view(self):
        """Add custom elements to module views.
        Returns:
            list: List of HTML strings to be inserted into the view
        """
        pass

    @hookspec
    def get_model(self, base_model):
        """Get module's model that extends the base model.
        Args:
            base_model: The base model instance to extend
        Returns:
            list: List containing the module model instance
        """
        pass

    @hookspec
    def get_routes(self):
        """Get module's routes and blueprints.
        Returns:
            list: List containing (blueprint, url_prefix) tuples
        """
        pass 