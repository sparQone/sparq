# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module controllers for onboarding functionality.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import render_template
from flask_login import login_required

from . import blueprint


@blueprint.route("/onboarding")
@login_required
def onboarding():
    """Onboarding page (coming soon)"""
    return render_template(
        "people-coming-soon.html",
        active_page="onboarding",
        title="Onboarding",
        module_home="people_bp.people_home",
    )
