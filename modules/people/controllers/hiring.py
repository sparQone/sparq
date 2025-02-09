from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/hiring")
@login_required
def hiring():
    return render_template(
        "people-coming-soon.html",
        active_page="hiring",
        title="Hiring",
        module_home="people_bp.people_home",
    )