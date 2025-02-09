from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/dashboard")
@login_required
def dashboard():
    """People dashboard page"""
    return render_template(
        "people-dashboard.html", active_page="dashboard", module_home="people_bp.people_home"
    )