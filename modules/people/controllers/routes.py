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

from flask import render_template, request, redirect, url_for, flash, current_app, g
from flask_login import login_required, current_user
from modules.core.models.user import User
from ..models.employee import Employee, EmployeeType, EmployeeStatus
from system.db.database import db
from datetime import datetime
from . import blueprint

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
    
    return render_template("employees/index.html",
                        active_page='employees',
                        users=users,
                        module_home='people_bp.people_home',
                        plugin_html=combined_plugin_html)


@blueprint.route("/hiring")
@login_required
def hiring():
    return render_template("people-coming-soon.html",
                        active_page='hiring',
                        title="Hiring",
                        module_home='people_bp.people_home')

@blueprint.route("/onboarding")
@login_required
def onboarding():
    """Onboarding page (coming soon)"""
    return render_template("people-coming-soon.html",
                        active_page='onboarding',
                        title="Onboarding",
                        module_home='people_bp.people_home')

@blueprint.route("/dashboard")
@login_required
def dashboard():
    """People dashboard page"""
    return render_template("people-dashboard.html",
                        active_page='dashboard',
                        module_home='people_bp.people_home')

@blueprint.route("/time_tracking")
@login_required
def time_tracking():
    return render_template("people-coming-soon.html",
                        active_page='time_tracking',
                        title="Time Tracking",
                        module_home='people_bp.people_home')

@blueprint.route("/scheduling")
@login_required
def scheduling():
    return render_template("people-coming-soon.html",
                        active_page='scheduling',
                        title="Shift Scheduling",
                        module_home='people_bp.people_home')

@blueprint.route("/forms")
@login_required
def forms():
    return render_template("people-coming-soon.html",
                        active_page='forms',
                        title="Forms",
                        module_home='people_bp.people_home')

@blueprint.route("/reimbursement")
@login_required
def reimbursement():
    """Reimbursement page (coming soon)"""
    return render_template("people-coming-soon.html",
                        active_page='reimbursement',
                        title="Reimbursement",
                        module_home='people_bp.people_home')

@blueprint.route("/docs")
@login_required
def docs():
    return render_template("people-coming-soon.html",
                        active_page='docs',
                        title="Documents",
                        module_home='people_bp.people_home')

@blueprint.route("/knowledge")
@login_required
def knowledge():
    return render_template("people-coming-soon.html",
                        active_page='knowledge',
                        title="Knowledge Base",
                        module_home='people_bp.people_home')

@blueprint.route("/settings")
@login_required
def settings():
    return render_template("people-coming-soon.html",
                        active_page='settings',
                        title="Settings",
                        module_home='people_bp.people_home')


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
    
    return render_template('employees/add-modal.html', plugin_html=combined_plugin_html)

@blueprint.route('/employees/table')
@login_required 
def employees_table():
    """Return the employees table partial template"""
    # Query only users who have employee profiles, excluding admin
    users = User.query.join(Employee).filter(User.email != 'admin').all()
    return render_template('employees/table-partial.html', 
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
            
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return """
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    <strong>Error:</strong> An account with this email already exists.
                </div>
            """, 422
            
        # Create user with minimal required fields
        user = User.create(
            email=email,
            password=request.form.get('password'),
            first_name=request.form.get('first_name', ''),
            last_name=request.form.get('last_name', ''),
            is_admin=bool(request.form.get('is_admin', False))
        )
        print(f"User created: {user}")
        
        # Check if employee profile already exists
        existing_employee = Employee.query.filter_by(user_id=user.id).first()
        if existing_employee:
            db.session.rollback()
            return """
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-circle"></i>
                    An employee profile already exists for this user.
                </div>
            """, 422
            
        # Create employee profile
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
        users = User.query.join(Employee).filter(User.email != 'admin').all()
        return render_template('employees/table-partial.html', users=users)
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return f"""
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-circle"></i>
                Error creating employee: {str(e)}
            </div>
        """, 400


@blueprint.route('/employees/<int:user_id>', methods=['PUT'])
@login_required
def edit_employee_htmx(user_id):
    """Edit an employee via HTMX request"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Validate required fields
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if not email or not first_name or not last_name:
            return "All required fields must be filled out", 400
            
        # Check if email is changed and already exists
        if email != user.email and User.query.filter_by(email=email).first():
            return "An account with this email already exists", 400
        
        # Update user fields
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = bool(request.form.get('is_admin'))
        
        # Update password only if provided
        password = request.form.get('password')
        if password and password.strip():
            user.set_password(password)
        
        # Update employee profile if it exists
        if hasattr(user, 'employee_profile') and user.employee_profile:
            user.employee_profile.department = request.form.get('department', '')
            user.employee_profile.position = request.form.get('position', '')
            if request.form.get('type'):
                try:
                    user.employee_profile.type = EmployeeType[request.form.get('type')]
                except KeyError:
                    return f"Invalid employee type: {request.form.get('type')}", 400
            
        db.session.commit()
        
        # Query only users who have employee profiles, excluding admin
        users = User.query.join(Employee).filter(User.email != 'admin').all()
        return render_template('employees/table-partial.html', users=users)
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating employee: {str(e)}")  # Add logging
        return f"Error updating employee: {str(e)}", 400

@blueprint.route('/employees/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete a user and their employee profile"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Delete employee profile if it exists
        if hasattr(user, 'employee_profile'):
            db.session.delete(user.employee_profile)
            
        db.session.delete(user)
        db.session.commit()
        
        users = User.query.join(Employee).filter(User.email != 'admin').all()
        return render_template('employees/table-partial.html', users=users)
    except Exception as e:
        return str(e), 400 

@blueprint.route("/employees/<int:employee_id>")
@login_required
def employee_details(employee_id):
    """Employee details page"""
    employee = Employee.query.get_or_404(employee_id)
    
    return render_template("employees/details.html",
                        employee=employee,
                        active_page='employees',
                        module_home='people_bp.people_home')

@blueprint.route("/employees/<int:employee_id>/edit/<field>", methods=['GET'])
@login_required
def edit_field(employee_id, field):
    """Get edit modal for a specific field"""
    employee = Employee.query.get_or_404(employee_id)
    
    field_labels = {
        'name': 'Name',
        # Add other fields here as we expand
    }
    
    return render_template(
        'employees/edit-field-modal.html',
        employee=employee,
        field=field,
        field_label=field_labels.get(field, field.title())
    )

@blueprint.route("/employees/<int:employee_id>/update/<field>", methods=['PUT'])
@login_required
def update_field(employee_id, field):
    """Update a specific field"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        if field == 'name':
            employee.user.first_name = request.form.get('first_name')
            employee.user.last_name = request.form.get('last_name')
            db.session.commit()
            
            # Return just the updated field HTML
            return f"""
            <div class="editable-field" data-field="name">
                <h1>
                    <span class="field-value">{employee.user.first_name} {employee.user.last_name}</span>
                    <button class="edit-btn" 
                            hx-get="{url_for('people_bp.edit_field', employee_id=employee.id, field='name')}"
                            hx-target="#modal-container"
                            hx-swap="innerHTML">
                        <i class="fas fa-edit"></i>
                    </button>
                </h1>
            </div>
            """
            
        return "Field not supported", 400
        
    except Exception as e:
        db.session.rollback()
        return str(e), 400 