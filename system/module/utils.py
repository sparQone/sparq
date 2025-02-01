# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Utility functions for module management including status reporting
#     and module information formatting.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import os
from .loader import ModuleLoader

def print_module_status(manifests, errors=None):
    """Print formatted table of module status"""
    # Only print status in main process (not reloader)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        return
        
    if not manifests:
        print("\nNo modules loaded!")
        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"ERROR: {error}")
        return

    # Calculate column widths
    module_width = max(len(m['name']) for m in manifests.values()) + 2
    type_width = max(len(m['type']) for m in manifests.values()) + 2
    
    # Print header
    print("\nLoading modules:")
    print("-" * (module_width + type_width + 15))
    print(f"{'Module':<{module_width}}{'Type':<{type_width}}Status")
    print("-" * (module_width + type_width + 15))
    
    # Print each module
    for manifest in manifests.values():
        status = "Enabled" if manifest.get('enabled', False) else "Disabled"
        print(f"{manifest['name']:<{module_width}}"
              f"{manifest['type']:<{type_width}}"
              f"{status}")
    print("-" * (module_width + type_width + 15))
    
    # Print any errors
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"ERROR: {error}")
    print()


def initialize_modules():
    """Initialize and validate required modules
    
    Returns:
        ModuleLoader: Initialized module loader instance
        
    Raises:
        SystemExit: If required modules are missing
    """
    # Load modules
    module_loader = ModuleLoader()
    module_loader.discover_modules()
    
    # Check for required modules
    required_modules = ['CoreModule', 'PeopleModule']
    loaded_modules = [m.__class__.__name__ for m in module_loader.modules]
    missing_modules = [m for m in required_modules if m not in loaded_modules]
    
    # Collect all errors
    errors = []
    if module_loader.errors:
        errors.extend(module_loader.errors)
    if missing_modules:
        errors.append(f"Required modules not found: {', '.join(missing_modules)}")
    
    # Print module status table with any errors
    print_module_status(module_loader.manifests, errors)
    
    # Exit if there are critical errors
    if missing_modules:
        print("Application cannot start without core and people modules.")
        os._exit(1)
        
    return module_loader 