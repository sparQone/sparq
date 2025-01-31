# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Expense module class that implements expense tracking and management.
#     Handles route registration and database initialization for the
#     expense management system.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from system.module.module_manager import hookimpl
from system.db.database import db

class ExpenseModule:
    def register_blueprint(self, blueprint, url_prefix):
        self._blueprint = blueprint
        self._url_prefix = url_prefix
        
    def get_routes(self):
        return [(self._blueprint, self._url_prefix)]
