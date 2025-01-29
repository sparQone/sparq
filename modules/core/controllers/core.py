from flask import Blueprint, render_template, jsonify, current_app, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from ..models.user import User
from system.db.database import db
import os
import importlib

# Create blueprint
blueprint = Blueprint(
    'core_bp', 
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

def admin_required(f):
    """Decorator to require admin access for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'error')
            return redirect(url_for('core_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def enrich_module_data(modules):
    """Add additional module data like colors"""
    enriched = []
    for module in modules:
        # Get the manifest data
        manifest = module if isinstance(module, dict) else module.get('manifest', {})
        
        # Create enriched module using manifest data
        enriched_module = {
            'name': manifest.get('name'),
            'type': manifest.get('type'),
            'main_route': manifest.get('main_route'),
            'icon_class': manifest.get('icon_class'),
            'color': manifest.get('color', '#6c757d'),
            'enabled': manifest.get('enabled', True)
        }
        
        # Only add if we have at least a name and type
        if enriched_module['name'] and enriched_module['type']:
            enriched.append(enriched_module)
            
    return enriched

@blueprint.before_app_request
def before_request():
    """Make installed modules available to all templates and set current module"""
    g.installed_modules = current_app.config.get('INSTALLED_MODULES', [])
    if hasattr(g, 'installed_modules'):
        g.installed_modules = enrich_module_data(g.installed_modules)
        
        # Default core module data
        default_core = {
            'name': 'Core',
            'type': 'App',
            'main_route': '/core',
            'icon_class': 'fa-solid fa-home',
            'color': '#6c757d'
        }
        
        # Get current module from request path
        path = request.path.split('/')[1] or 'core'  # Default to core if root path
        
        # First try to find the current module
        current_module = next(
            (m for m in g.installed_modules if m.get('name', '').lower() == path.lower()),
            None
        )
        
        # If not found, try to find core module
        if not current_module:
            current_module = next(
                (m for m in g.installed_modules if m.get('name', '').lower() == 'core'),
                default_core  # Fall back to default core data
            )
        
        g.current_module = current_module

@blueprint.route("/")
@login_required
def home():
    """Redirect root to people dashboard"""
    return redirect(url_for('people_bp.people_home'))


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
            # Ensure the next page is safe and default to people dashboard
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

@blueprint.route("/settings")
@login_required
@admin_required
def settings():
    """Core settings page"""
    return render_template("settings/index.html",
                         module_name="Settings",
                         module_icon="fa-solid fa-cog",
                         module_home='core_bp.settings',
                         installed_modules=g.installed_modules)

@blueprint.route("/settings/apps")
@login_required
@admin_required
def manage_apps():
    """Apps management page"""
    modules_dir = "modules"
    modules = []
    
    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        
        if os.path.isdir(module_path) and not module_name.startswith('__'):
            try:
                manifest = importlib.import_module(f"modules.{module_name}.__manifest__").manifest
                manifest['enabled'] = not os.path.exists(os.path.join(module_path, '__DISABLED__'))
                modules.append(manifest)
            except Exception as e:
                print(f"Error loading manifest for {module_name}: {e}")
    
    return render_template("settings/apps.html", 
                         modules=sorted(modules, key=lambda x: x['name']),
                         module_name="Settings",
                         module_icon="fa-solid fa-cog",
                         module_home='core_bp.settings',
                         installed_modules=g.installed_modules)

@blueprint.route("/api/modules/toggle", methods=['POST'])
@login_required
@admin_required
def toggle_module():
    """Toggle module enabled/disabled state"""
    data = request.get_json()
    module_name = data.get('module')
    enabled = data.get('enabled')
    
    if not module_name:
        return jsonify({'error': 'Module name required'}), 400
        
    module_path = os.path.join('modules', module_name)
    disabled_file = os.path.join(module_path, '__DISABLED__')
    
    try:
        if enabled and os.path.exists(disabled_file):
            os.remove(disabled_file)
        elif not enabled and not os.path.exists(disabled_file):
            open(disabled_file, 'a').close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500