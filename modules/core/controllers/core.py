from flask import Blueprint, render_template, jsonify, current_app, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user, login_required, current_user
from ..models.core import Core
from modules.people.models.user import User

# Create blueprint
blueprint = Blueprint(
    'core_bp', 
    __name__,
    template_folder='../views/templates'
)

@blueprint.before_app_request
def before_request():
    """Make installed modules available to all templates"""
    g.installed_modules = current_app.config.get('INSTALLED_MODULES', [])

@blueprint.route("/")
@login_required
def home():
    """Render the apps dashboard as the home page"""
    return render_template("apps.html", 
                         module_name="Core",
                         module_icon="fa-solid fa-home",
                         module_home='core_bp.home',
                         installed_modules=g.installed_modules)

@blueprint.route("/core")
@login_required
def core_home():
    """Core module home page with form"""
    # Get plugin HTML and ensure it's a list of strings
    plugin_html = current_app.module_loader.pm.hook.modify_view()
    if not plugin_html:
        plugin_html = []
    
    # Flatten the list of lists into a single list of strings
    flattened_html = [item for sublist in plugin_html for item in (sublist if isinstance(sublist, list) else [sublist])]
    
    # Join all plugin HTML fragments with newlines for better formatting
    combined_plugin_html = "\n".join(filter(None, flattened_html))
    
    return render_template("form.html", plugin_html=combined_plugin_html)

@blueprint.route("/save", methods=['POST'])
def save():
    """Handle form submission"""
    # Get plugin models
    plugin_models = current_app.module_loader.pm.hook.get_model(base_model=Core())
    
    # Use the last plugin model if available, otherwise use base model
    model = plugin_models[-1][0] if plugin_models else Core()
    
    # Save the data
    model.save(request.form)
    return redirect(url_for('core_bp.core_home'))

def icon_class_filter(mod):
    """Returns a Font Awesome class string based on module name"""
    name = mod.get("name", "").lower()
    if "core" in name:
        return "fa-solid fa-home"
    elif "clock" in name:
        return "fa-regular fa-clock"
    elif "weather" in name:
        return "fa-solid fa-cloud-sun-rain"
    elif "nickname" in name:
        return "fa-solid fa-user-tag"
    return "fa-solid fa-puzzle-piece"

@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('people_bp.people_home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = User.get_by_email(email)
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            # Ensure the next page is safe and default to people app
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('people_bp.people_home')
            return redirect(next_page)
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('core_bp.login'))

@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if User.get_by_email(email):
            flash('Email already registered', 'error')
            return render_template('register.html')

        try:
            User.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('core_bp.login'))
        except Exception as e:
            flash('Registration failed', 'error')
            
    return render_template('register.html') 