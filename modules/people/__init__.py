from flask import Blueprint
from .controllers.people import blueprint as people_blueprint
from .module import PeopleModule

# Create module instance
module_instance = PeopleModule()

# Register routes
module_instance.register_blueprint(people_blueprint, url_prefix='/people') 