from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/docs")
@login_required
def docs():
    """Docs page (coming soon)"""
    return render_template(
        "people-coming-soon.html",
        active_page="docs",
        title="Docs",
        module_home="people_bp.people_home",
    )