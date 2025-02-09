from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/scheduling")
@login_required
def scheduling():
    return render_template(
        "people-coming-soon.html",
        active_page="scheduling",
        title="Shift Scheduling",
        module_home="people_bp.people_home",
    )
