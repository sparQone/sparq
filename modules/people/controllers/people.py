from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g
from flask_login import login_required, current_user
from ..models.user import User

# Create blueprint
blueprint = Blueprint(
    'people_bp', 
    __name__,
    template_folder='../views/templates'
)

@blueprint.route("/")
@login_required
def people_home():
    """People module dashboard page"""
    return render_template("dashboard.html",
                         active_page='dashboard',
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/employees")
@login_required
def employees():
    """Employees management page"""
    users = User.query.all()
    return render_template("people.html", 
                         active_page='employees',
                         users=users,
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/add", methods=['POST'])
@login_required
def add_user():
    """Add a new user"""
    try:
        User.create(
            email=request.form.get('email'),
            password=request.form.get('password'),
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            is_admin=bool(request.form.get('is_admin'))
        )
        flash('User added successfully', 'success')
    except Exception as e:
        flash(f'Error adding user: {str(e)}', 'error')
    
    return redirect(url_for('people_bp.employees'))

@blueprint.route("/delete/<int:user_id>", methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get_or_404(user_id)
        user.delete()
        flash('User deleted successfully', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('people_bp.employees'))

@blueprint.route("/hiring")
@login_required
def hiring():
    """Hiring page (coming soon)"""
    return render_template("hiring.html",
                         active_page='hiring',
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/onboarding")
@login_required
def onboarding():
    """Onboarding page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='onboarding',
                         title="Onboarding",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/dashboard")
@login_required
def dashboard():
    """People dashboard page"""
    return render_template("dashboard.html",
                         active_page='dashboard',
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/updates")
@login_required
def updates():
    """Updates page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='updates',
                         title="Updates",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/time-tracking")
@login_required
def time_tracking():
    """Time tracking page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='time_tracking',
                         title="Time Tracking",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/scheduling")
@login_required
def scheduling():
    """Shift scheduling page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='scheduling',
                         title="Shift Scheduling",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/forms")
@login_required
def forms():
    """Forms page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='forms',
                         title="Forms",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/reimbursement")
@login_required
def reimbursement():
    """Reimbursement page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='reimbursement',
                         title="Reimbursement",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/docs")
@login_required
def docs():
    """Documents page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='docs',
                         title="Documents",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/knowledge")
@login_required
def knowledge():
    """Knowledge base page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='knowledge',
                         title="Knowledge Base",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/settings")
@login_required
def settings():
    """Settings page (coming soon)"""
    return render_template("coming_soon.html",
                         active_page='settings',
                         title="Settings",
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules) 