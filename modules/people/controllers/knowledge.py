
from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/knowledge")
@login_required
def knowledge():
    return render_template(
        "people-coming-soon.html",
        active_page="knowledge",
        title="Knowledge",
        module_home="people_bp.people_home",
    )