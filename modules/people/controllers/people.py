from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g
from flask_login import login_required, current_user
from ..models.user import User

# Create blueprint
blueprint = Blueprint(
    'people_bp', 
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

# Add these constants at the top of the file
MODULE_NAME = "People"
MODULE_ICON = "fa-solid fa-users"
MODULE_HOME = 'people_bp.dashboard'

@blueprint.route("/")
@login_required
def people_home():
    """People dashboard page"""
    module = {
        'name': 'People',
        'icon_class': 'fa-solid fa-users',
        'color': '#0d6efd',
        'type': 'App'
    }
    return render_template("people-dashboard.html",
                         module=module,
                         module_name="People",
                         module_icon="fa-solid fa-users",
                         module_home='people_bp.people_home',
                         installed_modules=g.installed_modules)

@blueprint.route("/employees")
@login_required
def employees():
    """Employees page"""
    users = User.query.all()
    return render_template("people-employees.html",
                         active_page='employees',
                         users=users,
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
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
    """Updates page (coming soon)"""
    return render_template("people-coming-soon.html",
                         active_page='updates',
                         title="Updates",
                         module_name=MODULE_NAME,
                         module_icon=MODULE_ICON,
                         module_home=MODULE_HOME,
                         page_icon="fa-solid fa-bell",
                         icon_color="#ffc107",
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