from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint(
    'appointments_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def appointments_home():
    """Appointments home page"""
    return render_template("coming_soon.html",
                         title="Appointments",
                         module_name="Appointments",
                         module_icon="fa-solid fa-calendar-check",
                         page_icon="fa-solid fa-calendar-check",
                         icon_color="#fd7e14",
                         module_home='appointments_bp.appointments_home',
                         installed_modules=g.installed_modules) 