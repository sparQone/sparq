from .controllers.people import blueprint

# Create module instance with routes
module_instance = type('PeopleModule', (), {
    'blueprint': blueprint,
    'get_routes': lambda self: [(blueprint, "/people")]
})() 