from flask import Blueprint, render_template, g
from flask_login import login_required
from datetime import datetime

# Create blueprint
blueprint = Blueprint(
    'clock_bp', 
    __name__, 
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def clock_home():
    """Clock page"""
    return render_template("clock.html",
                         module_name="Clock",
                         module_icon="fa-regular fa-clock",
                         module_home='clock_bp.clock_home',
                         installed_modules=g.installed_modules)
