# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     E-Sign module routes and controllers for the e-sign functionality.
#     Handles the main route and rendering of the e-sign home page.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from flask import render_template
from flask_login import login_required

blueprint = Blueprint(
    "esign_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)


@blueprint.route("/")
@login_required
def esign_home():
    """E-Sign home page"""
    return render_template("esign/index.html", title="E-Sign", module_home="esign_bp.esign_home")
