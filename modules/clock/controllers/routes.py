# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Clock module routes and controllers for the clock functionality.
#     Handles the main route and rendering of the clock home page.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from datetime import datetime

from flask import Blueprint
from flask import g
from flask import render_template
from flask_login import login_required

# Create blueprint
blueprint = Blueprint(
    "clock_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)


# Clock home page
@blueprint.route("/")
@login_required
def clock_home():
    """Clock page"""
    return render_template("clock/index.html", title="Clock", module_home="clock_bp.clock_home")
