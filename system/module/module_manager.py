import pluggy

# Define hookspecs and hookimpl markers
hookspec = pluggy.HookspecMarker("sparqone")
hookimpl = pluggy.HookimplMarker("sparqone")

class ModuleSpecs:
    @hookspec
    def init_database(self):
        """Optional: Initialize database tables and sample data for the module.
        This hook is called after all modules are loaded and the database
        connection is established.
        """
        pass 