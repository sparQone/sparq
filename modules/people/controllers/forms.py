from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/forms")
@login_required
def forms():
    return render_template(
        "people-coming-soon.html",
        active_page="forms",
        title="Forms",
        module_home="people_bp.people_home",
    )