from flask import Blueprint, render_template
import datetime

# Create blueprint
blueprint = Blueprint(
    'clock_bp', 
    __name__, 
    template_folder='../views/templates'
)

@blueprint.route("/")
def clock_home():
    """Display the digital clock"""
    now = datetime.datetime.now()
    return render_template(
        "clock.html",
        time=now.strftime("%H:%M:%S"),
        date=now.strftime("%Y-%m-%d")
    )
