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
from .hooks import ModuleSpecs


class ModuleLoader:
    """
    Manages module discovery, loading, and registration.
    """
    def __init__(self, app=None):
        self.app = app
        self.modules = []
        self.pm = pluggy.PluginManager("sparqone")
        self.pm.add_hookspecs(ModuleSpecs)
        self.manifests = {}
        self.errors = []

    def load_module(self, module_name):
        """Load a single module"""
        try:
            # Load manifest
            manifest = importlib.import_module(f"modules.{module_name}.__manifest__").manifest
            manifest_copy = manifest.copy()  # Create a copy to avoid modifying the original
            
            # Check if module is disabled
            module_path = os.path.join("modules", module_name)
            disabled_file = os.path.join(module_path, '__DISABLED__')
            is_enabled = not os.path.exists(disabled_file)
            manifest_copy['enabled'] = is_enabled
            
            if is_enabled:
                # Load the module only if enabled
                module = importlib.import_module(f"modules.{module_name}")
                if hasattr(module, 'module_instance'):
                    self.manifests[manifest_copy['name']] = manifest_copy  # Use module name as key
                    instance = module.module_instance
                    self.pm.register(instance)
                    self.modules.append(instance)
                    return True
                else:
                    self.errors.append(f"Module '{module_name}' has no module_instance")
            else:
                self.manifests[manifest_copy['name']] = manifest_copy  # Still track disabled modules
                
        except Exception as e:
            self.errors.append(f"Failed to load module '{module_name}': {str(e)}")
            return False

    def discover_modules(self):
        """Discover and load all modules in correct order"""
        modules_dir = "modules"
        
        # Get list of all potential modules
        module_names = [d for d in os.listdir(modules_dir) 
                       if os.path.isdir(os.path.join(modules_dir, d)) 
                       and not d.startswith('_')]
        
        # First load Core module
        if 'core' in module_names:
            self.load_module('core')
            module_names.remove('core')
        else:
            self.errors.append("Core module not found - required for system operation")
            return
        
        # Then load People module
        if 'people' in module_names:
            self.load_module('people')
            module_names.remove('people')
        else:
            self.errors.append("People module not found - required for system operation")
            return
        
        # Load remaining modules in any order
        for module_name in module_names:
            self.load_module(module_name)

    def register_routes(self, app):
        """Register routes from all modules"""
        for module in self.modules:
            if hasattr(module, 'get_routes'):
                routes = module.get_routes()
                for blueprint, url_prefix in routes:
                    app.register_blueprint(blueprint, url_prefix=url_prefix) 