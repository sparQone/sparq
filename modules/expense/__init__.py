# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Expense module initialization and route registration. Sets up expense
#     tracking and management functionality including expense reports and
#     approvals.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint

from .controllers.routes import blueprint as expense_blueprint
from .module import ExpenseModule

# Create module instance
module_instance = ExpenseModule()

# Register routes
module_instance.register_blueprint(expense_blueprint, url_prefix="/expense")
