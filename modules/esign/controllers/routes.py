from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint(
    'esign_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def esign_home():
    """E-Sign home page"""
    return render_template("coming_soon.html",
                         title="E-Sign",
                         module_name="E-Sign",
                         module_icon="fa-solid fa-file-signature",
                         page_icon="fa-solid fa-file-signature",
                         icon_color="#0dcaf0",
                         module_home='esign_bp.esign_home',
                         installed_modules=g.installed_modules) 