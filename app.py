import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')


from flask import Flask, request, jsonify, redirect, url_for
from system.module.module_loader import ModuleLoader
from flask_login import LoginManager
from system.db.database import db
from modules.people.models.user import User
import os

def create_app():
    app = Flask(__name__)
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
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
        return User.query.get(int(user_id))
    
    # Create database tables and seed admin user
    with app.app_context():
        db.create_all()
        # Seed admin user if not exists
        if not User.get_by_email('admin'):
            User.create(
                email='admin',
                password='admin',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            print("Created default admin user")
    
    # Initialize module loader
    module_loader = ModuleLoader()
    app.module_loader = module_loader
    module_loader.load_modules()
    
    # Store manifests in app config
    app.config['INSTALLED_MODULES'] = module_loader.manifests
    
    # Register routes
    module_loader.register_routes(app)
    
    # Register Jinja filters
    core_module = next(
        (m for m in module_loader.modules 
         if m.__class__.__name__ == 'CoreModule'), 
        None
    )
    if core_module:
        app.jinja_env.filters['icon_class'] = core_module.icon_class_filter
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
