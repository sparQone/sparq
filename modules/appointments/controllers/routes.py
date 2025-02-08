# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Appointments module route handlers for scheduling functionality.
#     Implements CRUD operations and view logic for appointment management.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from flask import g
from flask import render_template
from flask_login import current_user
from flask_login import login_required

# Create blueprint with correct template folder
blueprint = Blueprint(
    "appointments_bp",
    __name__,
    template_folder="../views/templates",  # Point to the templates folder
    static_folder="../static",  # Point to static folder for CSS/JS/etc
)


@blueprint.route("/")
@login_required
def appointments_home():
    """Appointments dashboard page"""
    return render_template(
        "appointments/index.html",
        title="Appointments",
        module_home="appointments_bp.appointments_home",
    )
