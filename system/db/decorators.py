# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Database decorators for model registration and tracking.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

class ModelRegistry:
    """Simple registry to track SQLAlchemy models across modules"""
    models = []
    registration_order = 1  # Track registration order
    
    # Define module loading order
    MODULE_ORDER = ['core', 'people']  # Core first, people second, rest alphabetically
    
    @classmethod
    def register(cls, model_class):
        """Decorator to register a model"""
        # Get proper module name from full path
        module_path = model_class.__module__.split('.')
        if 'modules' in module_path:
            module_name = module_path[module_path.index('modules') + 1]
        else:
            module_name = 'core'
            
        cls.models.append({
            'module': module_name,
            'model': model_class.__name__,
            'table': model_class.__tablename__,
            'order': cls.registration_order
        })
        cls.registration_order += 1
        return model_class

    @classmethod
    def _get_module_order(cls, module_name):
        """Helper to determine module sort order"""
        try:
            return cls.MODULE_ORDER.index(module_name)
        except ValueError:
            return len(cls.MODULE_ORDER)  # Put non-core/people modules last

    @classmethod
    def print_summary(cls):
        """Print a summary of all registered models"""
        print("\nDatabase Model Registry:")
        print("------------------------")
        
        # Find the longest names for padding
        max_module = max(len(m['module']) for m in cls.models)
        max_model = max(len(m['model']) for m in cls.models)
        
        # Print header
        print(f"\nModule{' ' * (max_module - 6)}   Model{' ' * (max_model - 2)}   Table")
        print(f"{'-' * max_module}   {'-' * max_model}   {'-' * 20}")
        
        # Sort by module order first, then by registration order
        for model in sorted(cls.models, key=lambda x: (cls._get_module_order(x['module']), x['module'], x['order'])):
            module_pad = ' ' * (max_module - len(model['module']))
            model_pad = ' ' * (max_model - len(model['model']))
            print(f"{model['module']}{module_pad}   {model['model']}{model_pad}   {model['table']}")
        print() 