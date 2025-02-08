# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module controllers for update functionality.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import json
import time

from flask import Response as FlaskResponse
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask import stream_with_context
from flask_login import current_user
from flask_login import login_required

from system.db.database import db

from ..models.update import Reply
from ..models.update import Update
from ..models.update import UpdateType
from . import blueprint


@blueprint.route("/updates")
@login_required
def updates():
    """Company updates page"""
    updates = Update.query.order_by(Update.pinned.desc(), Update.created_at.desc()).all()
    return render_template(
        "updates/index.html",
        updates=updates,
        update_types=UpdateType,
        active_page="updates",
        title="Company Updates",
        module_home="people_bp.people_home",
    )


@blueprint.route("/updates", methods=["POST"])
@login_required
def create_update():
    """Create a new update"""
    try:
        data = request.form
        update = Update(
            user_id=current_user.id,
            type=UpdateType[data["type"]],
            content=data["content"],
            pinned="pin" in data,
        )
        db.session.add(update)
        db.session.commit()

        # Emit update event with debug info after response
        current_app.socketio.emit("updates_changed", {"update_id": update.id}, include_self=True)

        return response
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@blueprint.route("/updates/<int:update_id>/pin", methods=["POST"])
@login_required
def toggle_pin(update_id):
    """Toggle pin status of an update"""
    update = Update.query.get_or_404(update_id)
    update.pinned = not update.pinned
    db.session.commit()
    return jsonify({"status": "success", "pinned": update.pinned})


@blueprint.route("/updates/<int:update_id>/like", methods=["POST"])
@login_required
def toggle_like(update_id):
    """Toggle like status of an update"""
    update = Update.query.get_or_404(update_id)
    if current_user in update.likes:
        update.likes.remove(current_user)
    else:
        update.likes.append(current_user)
    db.session.commit()
    return jsonify({"status": "success", "likes_count": len(update.likes)})


@blueprint.route("/updates/list")
@login_required
def get_updates():
    """Get updates list for HTMX"""
    updates = Update.query.order_by(Update.created_at.desc()).all()
    return render_template(
        "updates/partials/updates_list.html", updates=updates, current_user=current_user
    )


@blueprint.route("/updates/<int:update_id>/replies", methods=["POST"])
@login_required
def create_reply(update_id):
    """Create a new reply to an update"""
    try:
        update = Update.query.get_or_404(update_id)
        reply = Reply(update_id=update_id, user_id=current_user.id, content=request.form["content"])
        db.session.add(reply)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
