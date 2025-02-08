# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Expense module routes and controllers for the expense functionality.
#     Handles the main route and rendering of the expense home page.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from flask import g
from flask import render_template
from flask_login import login_required

blueprint = Blueprint(
    "expense_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)


@blueprint.route("/")
@login_required
def expense_home():
    return render_template(
        "expense/index.html", title="Expense", module_home="expense_bp.expense_home"
    )
