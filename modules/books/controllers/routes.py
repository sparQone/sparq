# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Books module routes and controllers for the books functionality.
#     Handles the main route and rendering of the books home page.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

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
    """Books home page"""
    return render_template("books-index.html",
                        title="Books",
                        module_name=g.current_module['name'],
                        module_icon=g.current_module['icon_class'],
                        page_icon=g.current_module['icon_class'],
                        icon_color=g.current_module['color'],
                        module_home='books_bp.books_home',
                        installed_modules=g.installed_modules) 