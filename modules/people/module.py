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

from system.db.database import db
from system.module.hooks import hookimpl

from .controllers import blueprint
from .hooks import PeopleHookSpecs
from .models import Channel
from .models import Employee


class PeopleModule:
    def __init__(self):
        self.blueprint = blueprint

    def get_routes(self):
        """Return list of routes to register"""
        return [(self.blueprint, "/people")]

    @hookimpl
    def init_database(self):
        """Initialize database tables and create sample data"""
        db.create_all()  # This will create only tables that haven't been created yet

        # Create sample employees
        Employee.create_sample_employees()

        # Create default channels
        Channel.create_default_channels()

    def register_specs(self, plugin_manager):
        """Register hook specifications and implementations"""
        plugin_manager.add_hookspecs(PeopleHookSpecs)
        plugin_manager.register(self)

    def replace_url(self, match):
        url = match.group(0)
        display_url = url[:50] + "..." if len(url) > 50 else url
        full_url = url if url.startswith(("http://", "https://")) else f"https://{url}"
        return f'<a href="{full_url}" target="_blank" rel="noopener noreferrer" class="chat-link">{display_url}</a>'


# Create module instance
module_instance = PeopleModule()
