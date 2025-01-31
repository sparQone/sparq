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

from flask import Blueprint, render_template, request, jsonify, g
from flask_login import login_required, current_user
from ..models.appointment import Appointment, AppointmentStatus
from system.db.database import db

# Create blueprint
blueprint = Blueprint(
    'appointments_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route('/')
@login_required
def appointments_home():
    """Appointments dashboard page"""
    return render_template('appointments-dashboard.html',
                         module_name=g.current_module['name'],
                         module_icon=g.current_module['icon_class'],
                         installed_modules=g.installed_modules) 