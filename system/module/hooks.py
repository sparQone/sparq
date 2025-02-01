# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Module management system that defines hook specifications and implements
#     the plugin architecture for module extensibility. Provides core hooks
#     for database initialization and other module lifecycle events.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import pluggy

# Define hookspecs and hookimpl markers
hookspec = pluggy.HookspecMarker("sparqone")
hookimpl = pluggy.HookimplMarker("sparqone")

class ModuleSpecs:
    @hookspec
    def init_database(self):
        """Optional: Initialize database tables and sample data for the module.
        This hook is called after all modules are loaded and the database
        connection is established.
        """
        pass 