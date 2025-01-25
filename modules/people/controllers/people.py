from flask import Blueprint, render_template
from ..models.user import User

# Create blueprint
blueprint = Blueprint(
    'people_bp', 
    __name__,
    template_folder='../views/templates'
)

@blueprint.route("/")
def people_home():
    """People module home page"""
    return render_template("people.html") 