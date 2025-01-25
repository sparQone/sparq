import os
import importlib
import pluggy
from .module_manager import ModuleSpecs

class ModuleLoader:
    def __init__(self):
        self.pm = pluggy.PluginManager("sparqone")
        self.pm.add_hookspecs(ModuleSpecs)
        self.manifests = []
        self.modules = []
        
    def load_modules(self, modules_dir="modules"):
        """Load modules dynamically from the modules folder"""
        if not os.path.exists(modules_dir):
            print(f"Modules folder '{modules_dir}' does not exist!")
            return
            
        for module_name in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, module_name)
            
            if os.path.isdir(module_path) and not module_name.startswith('__'):
                try:
                    # Import the module and its manifest
                    module = importlib.import_module(f"modules.{module_name}")
                    manifest = importlib.import_module(f"modules.{module_name}.__manifest__").manifest
                    
                    if hasattr(module, 'module_instance'):
                        instance = module.module_instance
                        self.pm.register(instance)
                        self.manifests.append(manifest)
                        self.modules.append(instance)
                        print(f"Successfully loaded module: {module_name}")
                except Exception as e:
                    print(f"Failed to load module {module_name}: {str(e)}")

    def register_routes(self, app):
        """Register routes from all modules"""
        for module in self.modules:
            if hasattr(module, 'get_routes'):
                routes = module.get_routes()
                for blueprint, url_prefix in routes:
                    app.register_blueprint(blueprint, url_prefix=url_prefix) 