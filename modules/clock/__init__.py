# This file can be empty or contain clock module initialization logic

from .controllers.clock import blueprint

# Create module instance with routes
module_instance = type('ClockModule', (), {
    'blueprint': blueprint,
    'get_routes': lambda self: [(blueprint, "/clock")]
})()
