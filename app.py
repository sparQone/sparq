# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Main application entry point that initializes Flask app, configures 
#     database, loads modules, and sets up core functionality including 
#     authentication and module management.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

from flask import Flask, request, jsonify, redirect, url_for, g, session
from system.module.loader import ModuleLoader
from system.module.utils import print_module_status, initialize_modules
from flask_login import LoginManager, current_user
from system.db.database import db
from modules.core.models.user import User
from modules.core.models.user_setting import UserSetting
from system.i18n.translation import preload_translations, translate, format_date, format_number
import os
from system.db.decorators import ModelRegistry

def get_locale():
    """Get locale from URL parameters or default to English"""
    return request.args.get('lang', 'en')

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
    login_manager.init_app(app)
    login_manager.login_view = 'core_bp.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from flask import current_app
        return db.session.get(User, int(user_id))
    
    # Initialize and validate modules
    module_loader = initialize_modules()
    app.module_loader = module_loader  # Store module_loader in app instance
    
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
    
    # Add translation function to globals and formatting functions as filters
    app.jinja_env.globals['_'] = translate
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_number'] = format_number
    
    @app.before_request
    def before_request():
        # Set current module based on URL path
        path = request.path.split('/')[1] or 'core'
        g.current_module['name'] = path.lower()
        
        # Language selection priority:
        # 1. URL parameter
        # 2. Session
        # 3. User setting (if authenticated)
        # 4. Default language
        g.lang = request.args.get('lang') or \
                 session.get('lang') or \
                 (UserSetting.get(current_user.id, 'language') if current_user.is_authenticated else None) or \
                 app.config.get('DEFAULT_LANGUAGE', 'en')
        
        # Store in session if not already there
        if 'lang' not in session or session['lang'] != g.lang:
            session['lang'] = g.lang
    
    # Load translations after app is fully configured
    with app.app_context():
        preload_translations()
    
    return app

if __name__ == '__main__':
    flask_app = create_app()

    # After create_app() and before app.run()
    ModelRegistry.print_summary()

    flask_app.run(debug=True, host="0.0.0.0", port=8000)
    



