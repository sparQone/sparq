import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')


from flask import Flask, request, jsonify, redirect, url_for
from system.module.module_loader import ModuleLoader
from flask_login import LoginManager
from system.db.database import db
from modules.core.models.user import User
import os

def create_app():
    app = Flask(__name__, 
                template_folder='modules/core/views/templates',
                static_folder='modules/core/views/assets',
                static_url_path='/assets')
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'core_bp.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login"""
        return User.get_by_id(int(user_id))
    
    # Create module loader
    module_loader = ModuleLoader()
    
    # Initialize module loader with app and store it
    module_loader.app = app
    app.module_loader = module_loader  # Store module_loader in app
    
    # Load modules
    module_loader.load_modules()
    
    # Check for required modules
    required_modules = ['CoreModule', 'PeopleModule']
    loaded_modules = [m.__class__.__name__ for m in module_loader.modules]
    missing_modules = [m for m in required_modules if m not in loaded_modules]
    
    if missing_modules:
        print(f"ERROR: Required modules not found: {', '.join(missing_modules)}")
        print("Application cannot start without core and people modules.")
        os._exit(1)
    
    # Store manifests in app config
    app.config['INSTALLED_MODULES'] = module_loader.manifests
    
    # Register routes
    module_loader.register_routes(app)
    
    # Create/update database tables AFTER loading all modules
    with app.app_context():
        db.create_all()
        
        # Call init_database hooks for all modules
        module_loader.pm.hook.init_database()
        
        # Then check for admin user
        if not User.get_by_email('admin'):
            User.create(
                email='admin',
                password='admin',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            print("Created default admin user")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8080)
