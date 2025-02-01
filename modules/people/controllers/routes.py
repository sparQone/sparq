# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module route handlers for employee management functionality.
#     Implements CRUD operations and view logic for employee data.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g
from flask_login import login_required, current_user
from modules.core.models.user import User
from ..models.employee import Employee, EmployeeType, EmployeeStatus
from system.db.database import db
from datetime import datetime

# Module constants
MODULE_NAME = "People"
MODULE_ICON = "fa-solid fa-users"
MODULE_HOME = "people_bp.people_home"

# Create blueprint
blueprint = Blueprint(
    'people_bp', 
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def people_home():
    """People dashboard page"""
    return render_template("people-dashboard.html",
                        title=g.current_module['name'],
                        module_name=g.current_module['name'],
                        module_icon=g.current_module['icon_class'],
                        page_icon=g.current_module['icon_class'],
                        icon_color=g.current_module['color'],
                        module_home='people_bp.people_home',
                        installed_modules=g.installed_modules)

@blueprint.route("/employees")
@login_required
def employees():
    """Employees page"""
    # Query only users who have employee profiles, excluding admin
    users = User.query.join(Employee).filter(User.email != 'admin').all()
    
    # Get plugin HTML for the form
    plugin_html = current_app.module_loader.pm.hook.modify_new_employee_form()
    if not plugin_html:
        plugin_html = []
    
    # Flatten and combine plugin HTML
    flattened_html = [item for sublist in plugin_html for item in (sublist if isinstance(sublist, list) else [sublist])]
    combined_plugin_html = "\n".join(filter(None, flattened_html))
    
    return render_template("people-employees.html",
                         active_page='employees',
                         users=users,
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         plugin_html=combined_plugin_html,
                         installed_modules=g.installed_modules)


@blueprint.route("/hiring")
@login_required
def hiring():
    return render_template("people-coming-soon.html",
                         active_page='hiring',
                         title="Hiring",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-user-plus",
                         icon_color="#198754",
                         installed_modules=g.installed_modules)

@blueprint.route("/onboarding")
@login_required
def onboarding():
    """Onboarding page (coming soon)"""
    return render_template("people-coming-soon.html",
                         active_page='onboarding',
                         title="Onboarding",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-handshake",
                         icon_color="#6610f2",
                         installed_modules=g.installed_modules)

@blueprint.route("/dashboard")
@login_required
def dashboard():
    """People dashboard page"""
    return render_template("people-dashboard.html",
                         active_page='dashboard',
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         installed_modules=g.installed_modules)

@blueprint.route("/updates")
@login_required
def updates():
    """Company updates page"""
    return render_template("people-updates.html",
                         active_page='updates',
                         title="Company Updates",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         installed_modules=g.installed_modules)

@blueprint.route("/time_tracking")
@login_required
def time_tracking():
    return render_template("people-coming-soon.html",
                         active_page='time_tracking',
                         title="Time Tracking",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-clock",
                         icon_color="#dc3545",
                         installed_modules=g.installed_modules)

@blueprint.route("/scheduling")
@login_required
def scheduling():
    return render_template("people-coming-soon.html",
                         active_page='scheduling',
                         title="Shift Scheduling",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-calendar-alt",
                         icon_color="#0dcaf0",
                         installed_modules=g.installed_modules)

@blueprint.route("/forms")
@login_required
def forms():
    return render_template("people-coming-soon.html",
                         active_page='forms',
                         title="Forms",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-file-alt",
                         icon_color="#20c997",
                         installed_modules=g.installed_modules)

@blueprint.route("/reimbursement")
@login_required
def reimbursement():
    """Reimbursement page (coming soon)"""
    return render_template("people-coming-soon.html",
                         active_page='reimbursement',
                         title="Reimbursement",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-receipt",
                         icon_color="#20c997",
                         installed_modules=g.installed_modules)

@blueprint.route("/docs")
@login_required
def docs():
    return render_template("people-coming-soon.html",
                         active_page='docs',
                         title="Documents",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-folder",
                         icon_color="#6c757d",
                         installed_modules=g.installed_modules)

@blueprint.route("/knowledge")
@login_required
def knowledge():
    return render_template("people-coming-soon.html",
                         active_page='knowledge',
                         title="Knowledge Base",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-book",
                         icon_color="#d63384",
                         installed_modules=g.installed_modules)

@blueprint.route("/settings")
@login_required
def settings():
    return render_template("people-coming-soon.html",
                         active_page='settings',
                         title="Settings",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-cog",
                         icon_color="#6c757d",
                         installed_modules=g.installed_modules)


@blueprint.route('/employees/add/modal')
@login_required
def employee_add_modal():
    """Return the add employee modal template"""
    # Get plugin HTML for the form
    plugin_html = current_app.module_loader.pm.hook.modify_new_employee_form()
    if not plugin_html:
        plugin_html = []
    
    # Flatten and combine plugin HTML
    flattened_html = [item for sublist in plugin_html for item in (sublist if isinstance(sublist, list) else [sublist])]
    combined_plugin_html = "\n".join(filter(None, flattened_html))
    
    return render_template('employee-add-modal.html', plugin_html=combined_plugin_html)

@blueprint.route('/employees/table')
@login_required 
def employees_table():
    """Return the employees table partial template"""
    # Query only users who have employee profiles, excluding admin
    users = User.query.join(Employee).filter(User.email != 'admin').all()
    return render_template('employee-table-partial.html', 
                         users=users)

@blueprint.route('/employees/add', methods=['POST'])
@login_required
def add_employee_htmx():
    """Add a new employee via HTMX request"""
    try:
        # Validate required fields
        email = request.form.get('email')
        if not email:
            return "Email is required", 400
            
        # Create user with minimal required fields
        user = User.create(
            email=email,
            password=request.form.get('password'),
            first_name=request.form.get('first_name', ''),
            last_name=request.form.get('last_name', ''),
            is_admin=bool(request.form.get('is_admin', False))
        )
        print(f"User created: {user}")
        
        # Create employee profile if model exists
        if hasattr(user, 'employee_profile'):
            employee = Employee(
                user_id=user.id,
                department=request.form.get('department', ''),
                position=request.form.get('position', ''),
                type=EmployeeType[request.form.get('type', 'FULL_TIME')],
                status=EmployeeStatus.ACTIVE
            )
            db.session.add(employee)
            
        db.session.commit()
        
        # Return updated table
        users = User.query.all()
        return render_template('employee-table-partial.html', users=users)
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return str(e), 400

@blueprint.route('/employees/<int:user_id>/edit/modal')
@login_required
def employee_edit_modal(user_id):
    """Return the edit employee modal template"""
    user = User.query.get_or_404(user_id)
    
    # Get plugin HTML for the form - using the same hook as add form
    plugin_html = current_app.module_loader.pm.hook.modify_new_employee_form()
    if not plugin_html:
        plugin_html = []
    
    # Flatten and combine plugin HTML
    flattened_html = [item for sublist in plugin_html for item in (sublist if isinstance(sublist, list) else [sublist])]
    combined_plugin_html = "\n".join(filter(None, flattened_html))
    
    return render_template('employee-edit-modal.html', 
                         user=user, 
                         plugin_html=combined_plugin_html)

@blueprint.route('/employees/<int:user_id>', methods=['PUT'])
@login_required
def edit_employee_htmx(user_id):
    """Edit an employee via HTMX request"""
    try:
        user = User.query.get_or_404(user_id)
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.is_admin = bool(request.form.get('is_admin'))
        
        # Update password only if provided
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        # Update employee profile if it exists
        if hasattr(user, 'employee_profile') and user.employee_profile:
            user.employee_profile.department = request.form.get('department')
            user.employee_profile.position = request.form.get('position')
            if request.form.get('type'):
                user.employee_profile.type = EmployeeType[request.form.get('type')]
            
        db.session.commit()
        users = User.query.all()
        return render_template('employee-table-partial.html', users=users)
    except Exception as e:
        return str(e), 400

@blueprint.route('/employees/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete a user via HTMX request"""
    try:
        user = User.query.get_or_404(user_id)
        if user.email == 'admin':
            return "Cannot delete admin user", 400
            
        # First delete employee profile if it exists
        if hasattr(user, 'employee_profile') and user.employee_profile:
            if hasattr(user.employee_profile, 'nickname_data') and user.employee_profile.nickname_data:
                db.session.delete(user.employee_profile.nickname_data)
            db.session.delete(user.employee_profile)
            
        db.session.delete(user)
        db.session.commit()
        
        users = User.query.all()
        return render_template('employee-table-partial.html', users=users)
    except Exception as e:
        return str(e), 400 