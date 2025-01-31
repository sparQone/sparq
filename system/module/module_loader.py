# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Core module loading system that handles dynamic module discovery,
#     initialization, and registration. Manages plugin system and module hooks.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import os
import importlib
import pluggy
from .module_manager import ModuleSpecs

class ModuleLoader:
    def __init__(self, app=None):
        self.app = app
        self.modules = []
        self.pm = pluggy.PluginManager("sparqone")
        self.pm.add_hookspecs(ModuleSpecs)
        self.manifests = []
        
    def load_modules(self):
        """Load all modules from the modules directory"""
        modules_dir = "modules"
        
        print("\nLoading modules:")
        print("---------------")
        
        for module_name in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, module_name)
            
            if os.path.isdir(module_path) and not module_name.startswith('__'):
                try:
                    # Load manifest
                    manifest = importlib.import_module(f"modules.{module_name}.__manifest__").manifest
                    
                    # Check if module is disabled
                    disabled_file = os.path.join(module_path, '__DISABLED__')
                    is_enabled = not os.path.exists(disabled_file)
                    manifest['enabled'] = is_enabled
                    
                    # Get module type and status
                    module_type = manifest.get('type', 'Unknown')
                    status = "Enabled" if is_enabled else "Disabled"
                    
                    # Print module info with consistent formatting
                    print(f"- {manifest['name']} ({module_type}): {status}")
                    
                    if is_enabled:
                        # Load the module only if enabled
                        module = importlib.import_module(f"modules.{module_name}")
                        if hasattr(module, 'module_instance'):
                            self.manifests.append(manifest)
                            instance = module.module_instance
                            self.pm.register(instance)  # Register with plugin manager
                            self.modules.append(instance)
                        
                except Exception as e:
                    print(f"- {module_name}: Failed to load ({str(e)})")
        
        print("---------------\n")

    def register_routes(self, app):
        """Register routes from all modules"""
        for module in self.modules:
            if hasattr(module, 'get_routes'):
                routes = module.get_routes()
                for blueprint, url_prefix in routes:
                    app.register_blueprint(blueprint, url_prefix=url_prefix) 