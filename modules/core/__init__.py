# This file can be empty or contain core module initialization logic

from .controllers.core import blueprint, icon_class_filter

# Create module instance with routes and filter
module_instance = type('CoreModule', (), {
    'blueprint': blueprint,
    'get_routes': lambda self: [(blueprint, "/")],
    'icon_class_filter': staticmethod(icon_class_filter)
})()
