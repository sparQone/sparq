# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module class that implements HR and employee management features.
#     Handles route registration and database initialization for the
#     employee management system.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from system.module.hooks import hookimpl
from .hooks import PeopleHookSpecs
from system.db.database import db
from .models.employee import Employee
from .controllers import blueprint

class PeopleModule:
    def __init__(self):
        self.blueprint = blueprint

    def get_routes(self):
        """Return list of routes to register"""
        return [(self.blueprint, '/people')]

    @hookimpl
    def init_database(self):
        """Initialize database tables and create sample data"""
        db.create_all()  # This will create only tables that haven't been created yet
        
        # Create sample employees
        Employee.create_sample_employees()

    def register_specs(self, plugin_manager):
        """Register hook specifications and implementations"""
        plugin_manager.add_hookspecs(PeopleHookSpecs)
        plugin_manager.register(self)

# Create module instance
module_instance = PeopleModule() 