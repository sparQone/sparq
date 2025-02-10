# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module controllers for employee management.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import current_app, g, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import logging

from modules.core.models.user import User
from modules.people.models.employee import Employee, EmployeeType, EmployeeStatus, Gender
from modules.people.decorators import admin_required
from system.db.database import db
from . import blueprint

logger = logging.getLogger(__name__)

@blueprint.route("/")
@login_required
def people_home():
    """People dashboard page"""
    return render_template(
        "dashboard/index.html",
        title=g.current_module["name"],
        module_name=g.current_module["name"],
        module_icon=g.current_module["icon_class"],
        page_icon=g.current_module["icon_class"],
        icon_color=g.current_module["color"],
        module_home="people_bp.people_home",
        installed_modules=g.installed_modules,
    )

@blueprint.route("/dashboard")
@login_required
def dashboard():
    """People dashboard page"""
    return render_template(
        "dashboard/index.html", active_page="dashboard", module_home="people_bp.people_home"
    )

@blueprint.route("/employees")
@login_required
def employees():
    """Employees list page"""
    print(f"\nDEBUG: Current user: {current_user.id} - {current_user.email}")
    print(f"DEBUG: Is admin: {current_user.is_admin}")
    print(f"DEBUG: Has employee profile: {current_user.employee_profile is not None}")
    print(f"DEBUG: Template variables:")
    print(f"DEBUG: - current_user.is_admin: {current_user.is_admin}")
    print(f"DEBUG: - employee_id value: {current_user.employee_profile.id if current_user.employee_profile else 'None'}")
    print(f"DEBUG: - url: {url_for('people_bp.employee_detail', employee_id=current_user.employee_profile.id)}\n")
    users = User.query.join(Employee).filter(User.email != "admin").all()
    return render_template(
        "employees/index.html",
        active_page="employees",
        users=users,
        module_home="people_bp.people_home",
    )


@blueprint.route("/employees/new", methods=["GET"])
@login_required
@admin_required
def new_employee():
    """Show new employee form"""
    # Get all employees as potential managers
    potential_managers = Employee.query.join(User).order_by(User.first_name).all()
    
    return render_template(
        "employees/form.html",
        title="New Employee",
        employee=None,
        employee_types=EmployeeType,
        potential_managers=potential_managers,
        module_home="people_bp.people_home",
    )


@blueprint.route("/employees", methods=["POST"])
@login_required
@admin_required
def create_employee():
    """Create a new employee"""
    try:
        # Validate required fields
        email = request.form.get("email")
        if not email:
            flash("Email is required", "error")
            return redirect(url_for("people_bp.new_employee"))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists", "error")
            return redirect(url_for("people_bp.new_employee"))

        # Create user
        user = User.create(
            email=email,
            password=request.form.get("password"),
            first_name=request.form.get("first_name", ""),
            last_name=request.form.get("last_name", ""),
            is_admin=bool(request.form.get("is_admin", False)),
        )

        # Create employee profile
        employee = Employee(
            user_id=user.id,
            department=request.form.get("department", ""),
            position=request.form.get("position", ""),
            type=EmployeeType[request.form.get("type", "FULL_TIME")],
            status=EmployeeStatus.ACTIVE,
        )
        
        # Add manager if selected
        manager_id = request.form.get("manager_id")
        if manager_id:
            employee.manager_id = int(manager_id)
            
        db.session.add(employee)
        db.session.commit()

        flash("Employee created successfully", "success")
        return redirect(url_for("people_bp.employees"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error creating employee: {str(e)}", "error")
        return redirect(url_for("people_bp.new_employee"))


@blueprint.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_employee(employee_id):
    """Edit an employee"""
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == "POST":
        try:
            # Update user info
            employee.user.email = request.form.get("email")
            employee.user.first_name = request.form.get("first_name")
            employee.user.last_name = request.form.get("last_name")
            employee.user.is_admin = bool(request.form.get("is_admin"))
            
            # Update password if provided
            password = request.form.get("password")
            if password and password.strip():
                employee.user.set_password(password)
            
            # Update employee info
            employee.position = request.form.get("position")
            employee.department = request.form.get("department")
            employee.phone = request.form.get("phone")
            employee.salary = float(request.form.get("salary")) if request.form.get("salary") else None
            
            # Update address information
            employee.address = request.form.get("address")
            employee.city = request.form.get("city")
            employee.state = request.form.get("state")
            employee.zip_code = request.form.get("zip_code")
            
            # Handle dates
            start_date = request.form.get("start_date")
            if start_date:
                employee.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            birthday = request.form.get("birthday")
            if birthday:
                employee.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
            
            # Update type if provided
            if request.form.get("type"):
                employee.type = EmployeeType[request.form.get("type")]
            
            # Update gender if provided
            if request.form.get("gender"):
                employee.gender = Gender[request.form.get("gender")]
            
            # Update other fields
            employee.emergency_contact_name = request.form.get("emergency_contact_name")
            employee.emergency_contact_phone = request.form.get("emergency_contact_phone")
            employee.emergency_contact_relationship = request.form.get("emergency_contact_relationship")
            
            # Update manager
            manager_id = request.form.get("manager_id")
            if manager_id:
                employee.manager_id = int(manager_id)
            else:
                employee.manager_id = None
            
            db.session.commit()
            flash("Employee updated successfully", "success")
            return redirect(url_for("people_bp.employee_detail", employee_id=employee.id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error updating employee: {str(e)}", "error")
            return redirect(url_for("people_bp.edit_employee", employee_id=employee_id))
            
    # Get all employees except current one as potential managers
    potential_managers = Employee.query.filter(Employee.id != employee_id).join(User).order_by(User.first_name).all()
            
    return render_template(
        "employees/form.html",
        title="Edit Employee",
        employee=employee,
        employee_types=EmployeeType,
        potential_managers=potential_managers,
        module_home="people_bp.people_home",
    )


@blueprint.route("/employees/<int:employee_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_employee(employee_id):
    """Delete an employee"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        user = employee.user

        db.session.delete(employee)
        db.session.delete(user)
        db.session.commit()

        flash("Employee deleted successfully", "success")
        return redirect(url_for("people_bp.employees"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting employee: {str(e)}", "error")
        return redirect(url_for("people_bp.employees"))


@blueprint.route("/employees/<int:employee_id>/delete-modal", methods=["GET"])
@login_required
@admin_required
def delete_modal(employee_id):
    """Show delete confirmation modal"""
    return render_template(
        "employees/delete-modal.html",
        employee_id=employee_id
    )

@blueprint.route("/employees/<int:employee_id>")
@login_required
def employee_detail(employee_id):
    """Show employee details"""
    employee = Employee.query.get_or_404(employee_id)
    
    # Check if user is admin or viewing their own profile
    is_admin = current_user.is_admin
    is_self = current_user.id == employee.user_id
    
    # If not admin and not viewing own profile, show limited view
    if not is_admin and not is_self:
        return render_template(
            "employees/employee-view/details.html",  # Limited view template
            employee=employee,
            module_home="people_bp.people_home"
        )
    
    # Admin or self view gets full details
    return render_template(
        "employees/admin-view/details.html",  # Full admin view template
        employee=employee,
        module_home="people_bp.people_home"
    )
