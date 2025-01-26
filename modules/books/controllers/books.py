from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint(
    'books_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def books_home():
    return render_template("coming_soon.html",
                         title="Books",
                         module_name="Books",
                         module_icon="fa-solid fa-book-open",
                         module_home='books_bp.books_home',
                         installed_modules=g.installed_modules) 