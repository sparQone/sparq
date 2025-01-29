import os
import signal
from flask import jsonify
from flask_login import login_required
from modules.core.controllers.routes import blueprint  # Import the existing core blueprint

@blueprint.route('/api/restart', methods=['GET'])
@login_required
def restart():
    """Restart the Flask application by sending SIGTERM signal"""
    try:
        # Log the restart request
        print("Restart requested - sending SIGTERM")
        
        # Send SIGTERM to current process
        os.kill(os.getpid(), signal.SIGTERM)
        
        return jsonify({
            "status": "success",
            "message": "Restart signal sent"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500 