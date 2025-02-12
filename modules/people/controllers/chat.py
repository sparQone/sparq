from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room

from system.db.database import db

from ..models.chat import Channel
from ..models.chat import Chat
from . import blueprint


@blueprint.route("/chat")
@login_required
def chat():
    """Company chat page"""
    channels = Channel.query.all()
    default_channel = Channel.query.filter_by(name="general").first()
    if not default_channel:
        default_channel = Channel(
            name="general", description="General discussion channel", created_by_id=current_user.id
        )
        db.session.add(default_channel)
        db.session.commit()

    return render_template(
        "chat/index.html",
        active_page="chat",
        title="Company Chat",
        channels=channels,
        default_channel=default_channel,
        module_home="people_bp.people_home",
    )


@blueprint.route("/chat/channels/<channel_name>/messages")
@login_required
def get_channel_messages(channel_name):
    """Get messages for a specific channel"""
    try:
        channel = Channel.query.filter_by(name=channel_name).first_or_404()
        messages = channel.messages.order_by(Chat.created_at.asc()).all()
        return render_template(
            "chat/partials/chat_list.html",
            chats=messages,
            current_user=current_user,
            channel_description=channel.description,
        )
    except Exception as e:
        current_app.logger.error(f"Error getting channel messages: {str(e)}")
        return str(e), 500


@blueprint.route("/chat/channels", methods=["POST"])
@login_required
def create_channel():
    """Create a new channel"""
    try:
        name = request.form.get("name").lower().replace(" ", "-")
        description = request.form.get("description")
        is_private = bool(request.form.get("is_private", False))

        if not name:
            return "Channel name is required", 400

        # Check if channel already exists
        existing = Channel.query.filter_by(name=name).first()
        if existing:
            return "Channel already exists", 400

        channel = Channel(
            name=name, description=description, created_by_id=current_user.id, is_private=is_private
        )
        db.session.add(channel)
        db.session.commit()

        # Emit WebSocket event for new channel
        current_app.socketio.emit(
            "channel_created", {"name": channel.name, "description": channel.description}
        )

        return jsonify({"id": channel.id, "name": channel.name})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating channel: {str(e)}")
        return str(e), 400


@blueprint.route("/chat/create", methods=["POST"])
@login_required
def create_chat():
    """Create a new chat message"""
    try:
        content = request.form.get("content")
        channel_name = request.form.get("channel", "general")
        pinned = bool(request.form.get("pin", False))

        # Validate required fields
        if not content:
            return "Content is required", 400

        # Get or create channel
        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            return f"Channel {channel_name} not found", 404

        chat = Chat(
            content=content, author_id=current_user.id, channel_id=channel.id, pinned=pinned
        )
        db.session.add(chat)
        db.session.commit()

        # Emit WebSocket event with channel info
        current_app.socketio.emit("chat_changed", {"channel": channel_name}, room=channel_name)

        return ""
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating chat: {str(e)}")
        return str(e), 400


@blueprint.route("/chat/<int:chat_id>/pin", methods=["POST"])
@login_required
def toggle_pin(chat_id):
    """Toggle pin status of a chat"""
    try:
        chat = Chat.query.get_or_404(chat_id)
        if not current_user.is_admin and not chat.is_author:
            return jsonify({"error": "Unauthorized"}), 403

        is_pinned = chat.toggle_pin()
        current_app.socketio.emit(
            "chat_changed", {"channel": chat.channel.name}, room=chat.channel.name
        )
        return jsonify({"pinned": is_pinned})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@blueprint.route("/chat/<int:chat_id>", methods=["DELETE"])
@login_required
def delete_chat(chat_id):
    """Delete a chat message"""
    try:
        chat = Chat.query.get_or_404(chat_id)
        if not current_user.is_admin and not chat.is_author:
            return jsonify({"error": "Unauthorized"}), 403

        channel_name = chat.channel.name
        db.session.delete(chat)
        db.session.commit()

        current_app.socketio.emit("chat_changed", {"channel": channel_name}, room=channel_name)
        return "", 204
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# WebSocket event handlers
@current_app.socketio.on("join")
def on_join(data):
    """Join a chat channel"""
    channel = data.get("channel")
    if channel:
        join_room(channel)
        emit("status", {"msg": f"{current_user.first_name} has joined the channel."}, room=channel)


@current_app.socketio.on("leave")
def on_leave(data):
    """Leave a chat channel"""
    channel = data.get("channel")
    if channel:
        leave_room(channel)
        emit("status", {"msg": f"{current_user.first_name} has left the channel."}, room=channel)
