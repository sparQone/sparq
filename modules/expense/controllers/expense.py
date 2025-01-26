from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint(
    'expense_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def expense_home():
    return render_template("coming_soon.html",
                         title="Expense",
                         module_name="Expense",
                         module_icon="fa-solid fa-money-bill",
                         module_home='expense_bp.expense_home',
                         installed_modules=g.installed_modules) 