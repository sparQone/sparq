from flask import Blueprint, render_template, jsonify, current_app, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from system.db.database import db

# Create blueprint
blueprint = Blueprint(
    'core_bp', 
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

def enrich_module_data(modules):
    """Add additional module data like colors"""
    enriched = []
    for module in modules:
        # Get the manifest data and the module data
        manifest = module.get('manifest', {})
        
        # Create enriched module using both manifest and module data
        enriched_module = {
            'name': manifest.get('name') or module.get('name'),
            'type': manifest.get('type') or module.get('type'),
            'main_route': manifest.get('main_route') or module.get('main_route'),
            'icon_class': manifest.get('icon_class') or module.get('icon_class'),
            'color': manifest.get('color') or module.get('color', '#6c757d'),
            'manifest': manifest
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

@blueprint.route("/apps")
@login_required
def apps():
    """Render the apps grid page"""
    # Filter for App type only (exclude System modules) and sort alphabetically
    installed_modules = sorted(
        [m for m in g.installed_modules if m.get('type') == 'App'],
        key=lambda x: x.get('name', '')
    )
    
    return render_template("apps.html", 
                         module=g.current_module,
                         module_name="Apps",
                         module_icon="fa-solid fa-th",
                         module_home='core_bp.apps',
                         installed_modules=installed_modules)