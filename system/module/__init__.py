from flask import Blueprint
from .routes import bp as system_bp

def init_app(app):
    app.register_blueprint(system_bp)
