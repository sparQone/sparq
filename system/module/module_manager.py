import pluggy

# Define hookspecs and hookimpl markers
hookspec = pluggy.HookspecMarker("sparqone")
hookimpl = pluggy.HookimplMarker("sparqone")

class ModuleSpecs:
    @hookspec
    def get_model(self, base_model):
        """Get module's model that extends the base model.
        Args:
            base_model: The base model instance to extend
        Returns:
            list: List containing the module model instance
        """
        pass 