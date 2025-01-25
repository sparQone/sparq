import datetime
from flask import Blueprint, jsonify

clock_bp = Blueprint('clock_bp', __name__)

@clock_bp.route("/time")
def get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"current_time": now})

def init_module(app):
    app.register_blueprint(clock_bp, url_prefix="/clock")
    print("Clock module initialized.")
