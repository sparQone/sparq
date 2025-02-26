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

import logging
import os

from flask import Flask
from flask import current_app
from flask import g
from flask import request
from flask import session
from flask_login import LoginManager
from flask_login import current_user
from flask_socketio import SocketIO

from modules.core.models.group import Group
from modules.core.models.user import User
from modules.core.models.user_setting import UserSetting
from system.db.database import db
from system.db.decorators import ModelRegistry
from system.i18n.translation import format_date
from system.i18n.translation import format_number
from system.i18n.translation import preload_translations
from system.i18n.translation import translate
from system.module.utils import initialize_modules

# Configure logging to suppress fsevents debug messages
logging.getLogger('fsevents').setLevel(logging.WARNING)
logging.getLogger('watchdog.observers.fsevents').setLevel(logging.WARNING)

def get_locale():
    """Get locale from URL parameters or default to English"""
    return request.args.get("lang", "en")


def create_app():
    app = Flask(
        __name__,
        template_folder="modules/core/views/templates",
        static_folder="modules/core/views/assets",
        static_url_path="/assets",
    )

    # Configure logging
    logging.basicConfig(level=logging.WARNING)
    app.logger.setLevel(logging.WARNING)

    # Log handler to show warning and error messages in console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # Initialize SocketIO
    socketio = SocketIO(app)
    app.socketio = socketio  # Store for access in other modules

    # Configure SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    # Initialize extensions
    db.init_app(app)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "core_bp.login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Create/update database tables and initialize modules within app context
    with app.app_context():
        # Initialize and validate modules first
        module_loader = initialize_modules()
        app.module_loader = module_loader  # Store module_loader in app instance

        # Store manifests in app config
        app.config["INSTALLED_MODULES"] = module_loader.manifests

        # Register routes
        module_loader.register_routes(app)

        # Create all database tables
        db.create_all()

        # Create default groups if they don't exist
        Group.get_or_create("ALL", "Default group for all users", True)
        Group.get_or_create("ADMIN", "Administrators group", True)

        # Call init_database hooks for all modules
        module_loader.pm.hook.init_database()

        # Print model registry after all models are loaded
        ModelRegistry.print_summary()

    # Add translation function to globals and formatting functions as filters
    app.jinja_env.globals["_"] = translate
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["format_number"] = format_number

    @app.before_request
    def before_request():
        """Global request setup and initialization"""
        # 1. User Group Handling
        if current_user.is_authenticated:
            from modules.core.models.group import Group

            all_group = Group.get_or_create("ALL", "Default group for all users", True)
            if all_group not in current_user.groups:
                current_user.add_to_group(all_group)

        # 2. Module Context Setup
        g.installed_modules = current_app.config.get("INSTALLED_MODULES", {}).values()
        path = request.path.split("/")[1] or "core"

        # Find current module by matching the path against main_route
        current_module = next(
            (
                m for m in g.installed_modules 
                if m.get("main_route", "").strip("/").lower() == path.lower()
            ),
            next(
                (m for m in g.installed_modules if m.get("name", "").lower() == "core"),
                None,  # If neither path nor core module found, will be None
            ),
        )

        if current_module is None:
            # Log warning that module wasn't found
            app.logger.warning(f"Module not found for path: {path}")
            # Let the route handler deal with 404 if needed

        g.current_module = current_module

        # 3. Language Handling
        g.lang = (
            request.args.get("lang")
            or session.get("lang")
            or (
                UserSetting.get(current_user.id, "language")
                if current_user.is_authenticated
                else None
            )
            or app.config.get("DEFAULT_LANGUAGE", "en")
        )

        # Store language in session if changed
        if "lang" not in session or session["lang"] != g.lang:
            session["lang"] = g.lang

    # Load translations after app is fully configured
    with app.app_context():
        preload_translations()

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.socketio.run(flask_app, debug=True, host="0.0.0.0", port=8000)
