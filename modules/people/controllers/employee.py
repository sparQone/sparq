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
from flask_login import login_required
from datetime import datetime

from modules.core.models.user import User
from modules.people.models.employee import Employee, EmployeeType, EmployeeStatus, Gender
from system.db.database import db
from . import blueprint


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
    users = User.query.join(Employee).filter(User.email != "admin").all()
    return render_template(
        "employees/index.html",
        active_page="employees",
        users=users,
        module_home="people_bp.people_home",
    )


@blueprint.route("/employees/new", methods=["GET"])
@login_required
def new_employee():
    """Show new employee form"""
    return render_template(
        "employees/form.html",
        title="New Employee",
        employee=None,
        employee_types=EmployeeType,
        module_home="people_bp.people_home",
    )


@blueprint.route("/employees", methods=["POST"])
@login_required
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
            employee.address = request.form.get("address")
            employee.emergency_contact_name = request.form.get("emergency_contact_name")
            employee.emergency_contact_phone = request.form.get("emergency_contact_phone")
            employee.emergency_contact_relationship = request.form.get("emergency_contact_relationship")
            
            db.session.commit()
            flash("Employee updated successfully", "success")
            return redirect(url_for("people_bp.employee_detail", employee_id=employee.id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error updating employee: {str(e)}", "error")
            return redirect(url_for("people_bp.edit_employee", employee_id=employee_id))
            
    return render_template(
        "employees/form.html",
        title="Edit Employee",
        employee=employee,
        employee_types=EmployeeType,
        module_home="people_bp.people_home",
    )


@blueprint.route("/employees/<int:employee_id>/delete", methods=["POST"])
@login_required
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
    return render_template(
        "employees/details.html",
        employee=employee,
        module_home="people_bp.people_home"
    )

@blueprint.route("/employees/<int:employee_id>/edit-field/<field>", methods=["GET"])
@login_required
def edit_field(employee_id, field):
    """Show edit field modal"""
    employee = Employee.query.get_or_404(employee_id)
    field_label = field.replace('_', ' ').title()
    return render_template(
        "employees/edit-field-modal.html",
        employee=employee,
        field=field,
        field_label=field_label
    )

@blueprint.route("/employees/<int:employee_id>/update-field/<field>", methods=["PUT"])
@login_required
def update_field(employee_id, field):
    """Update employee field"""
    employee = Employee.query.get_or_404(employee_id)
    
    if field == 'name':
        employee.user.first_name = request.form.get('first_name')
        employee.user.last_name = request.form.get('last_name')
    # Add other field updates as needed
    
    try:
        db.session.commit()
        return render_template(
            "employees/field-value.html",
            employee=employee,
            field=field
        )
    except Exception as e:
        db.session.rollback()
        return str(e), 400 