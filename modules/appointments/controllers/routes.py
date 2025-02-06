# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Appointments module route handlers for scheduling functionality.
#     Implements CRUD operations and view logic for appointment management.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint, render_template, g
from flask_login import login_required, current_user

# Create blueprint with correct template folder
blueprint  = Blueprint(
    'appointments_bp', 
    __name__,
    template_folder='../views/templates',  # Point to the templates folder
    static_folder='../static'  # Point to static folder for CSS/JS/etc
)

@blueprint.route('/')
@login_required
def appointments_home():
    """Appointments dashboard page"""
    return render_template("coming_soon.html",
                        title="Appointments",
                        module_name=g.current_module['name'],
                        module_icon=g.current_module['icon_class'],
                        page_icon=g.current_module['icon_class'],
                        icon_color=g.current_module['color'],
                        module_home='appointments_bp.appointments_home',
                        installed_modules=g.installed_modules) 