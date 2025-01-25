# This file can be empty or contain weather module initialization logic

from .controllers.weather import blueprint

# Create module instance with routes
module_instance = type('WeatherModule', (), {
    'blueprint': blueprint,
    'get_routes': lambda self: [(blueprint, "/weather")]
})()
