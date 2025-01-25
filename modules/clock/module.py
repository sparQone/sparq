from flask import Blueprint, jsonify
import datetime
from system.module.module_manager import hookimpl

class ClockModule:
    def __init__(self):
        self.blueprint = Blueprint('clock_bp', __name__)
        self.setup_routes()

    def setup_routes(self):
        @self.blueprint.route("/")
        def clock_home():
            return jsonify({"message": "Welcome to Clock Module"})

        @self.blueprint.route("/time")
        def get_time():
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({"current_time": now})

    @hookimpl
    def get_routes(self):
        return [(self.blueprint, "/clock")]

    @hookimpl
    def modify_view(self):
        return [] 