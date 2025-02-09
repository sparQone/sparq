
from flask import render_template
from flask_login import login_required

from . import blueprint

@blueprint.route("/reimbursement")
@login_required
def reimbursement():
    return render_template(
        "people-coming-soon.html",
        active_page="reimbursement",
        title="Reimbursement",
        module_home="people_bp.people_home",
)   