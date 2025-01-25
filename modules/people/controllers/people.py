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
    """People module home page with user management"""
    users = User.query.all()
    return render_template("people.html", 
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
    
    return redirect(url_for('people_bp.people_home')) 