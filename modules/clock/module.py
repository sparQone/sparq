from flask import Blueprint, jsonify
import datetime
from modules.module_manager import hookimpl

class ClockModule:
    def __init__(self):
        self.blueprint = Blueprint('clock_bp', __name__)
        self.setup_routes()

    def setup_routes(self):
        @self.blueprint.route("/")  # Add root route
        def clock_home():
            """Clock module home page"""
            return jsonify({"message": "Welcome to Clock Module"})

        @self.blueprint.route("/time")
        def get_time():
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({"current_time": now})

    @hookimpl
    def get_routes(self):
        return [(self.blueprint, "/clock")]  # This maps /clock/* to the blueprint

    @hookimpl
    def get_manifest(self):
        return {
            'name': 'Clock',
            'version': '1.0.0',
            'main_route': '/clock',
            'icon_class': 'fa-regular fa-clock',
            'type': 'app'  # Clock is a standalone app
        }

    @hookimpl
    def modify_view(self):
        # Add clock widget to dashboard if needed
        return [] 