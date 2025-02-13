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
from modules.core.models.user import User

from ..models.chat import Channel
from ..models.chat import Chat
from ..models.chat import InteractionType
from ..models.chat import ChatMessageState
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
        ChatMessageState=ChatMessageState
    )


@blueprint.route("/chat/channels/<channel_name>/messages")
@login_required
def get_channel_messages(channel_name):
    """Get messages for a specific channel"""
    try:
        # Get query parameters
        before_id = request.args.get('before_id', type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # Get channel
        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            return f"Channel {channel_name} not found", 404
            
        # Build query - First get total count and latest ID
        total_messages = channel.messages.count()
        if total_messages == 0:
            return render_template(
                "chat/partials/chat_list.html",
                chats=[],
                current_user=current_user,
                channel_description=channel.description,
                ChatMessageState=ChatMessageState,
                has_more=False,
                oldest_id=None,
                channel_name=channel_name
            )
        
        # If before_id is not provided, get the latest messages
        if not before_id:
            messages = channel.messages.order_by(Chat.created_at.desc()).limit(limit).all()
            messages = messages[::-1]  # Reverse to show in ascending order
            has_more = channel.messages.filter(Chat.id < messages[0].id).first() is not None
            oldest_id = messages[0].id
        else:
            # Get messages before the given ID
            messages = channel.messages.filter(Chat.id < before_id).order_by(Chat.created_at.desc()).limit(limit).all()
            messages = messages[::-1]  # Reverse to show in ascending order
            has_more = channel.messages.filter(Chat.id < messages[0].id).first() is not None if messages else False
            oldest_id = messages[0].id if messages else None
            
        # Mark messages as read for the current user
        for message in messages:
            ChatMessageState.mark_message_read(current_user.id, message.id)
        db.session.commit()
        
        return render_template(
            "chat/partials/chat_list.html",
            chats=messages,
            current_user=current_user,
            channel_description=channel.description,
            ChatMessageState=ChatMessageState,
            has_more=has_more,
            oldest_id=oldest_id,
            channel_name=channel_name
        )
            
    except Exception as e:
        current_app.logger.error(f"Error getting channel messages: {str(e)}")
        return str(e), 500


@blueprint.route("/chat/channels", methods=["POST"])
@login_required
def create_channel():
    """Create a new channel"""
    try:
        name = request.form.get("name")
        if not name:
            return "Channel name is required", 400

        name = name.lower().replace(" ", "-")
        description = request.form.get("description")
        is_private = bool(request.form.get("is_private", False))

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
        current_app.socketio.emit("channel_created", {
            "name": channel.name, 
            "description": channel.description
        })  # No 'to' needed since this should go to everyone

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
        db.session.flush()  # Get the chat ID without committing
        
        # Create message states for all users except the author
        users = User.query.filter(User.id != current_user.id).all()
        for user in users:
            state = ChatMessageState(
                user_id=user.id,
                message_id=chat.id,
                channel_id=channel.id,
                interaction_type=InteractionType.READ,
                data={'last_read_message_id': None}  # None indicates unread
            )
            db.session.add(state)
        
        db.session.commit()

        # Debug: Log message creation
        current_app.logger.info(f"New message created in {channel_name} by user {current_user.id}")

        # Emit two events:
        # 1. To users in the channel to refresh their messages
        current_app.socketio.emit("chat_changed", {
            "channel": channel_name,
            "message_id": chat.id,
            "author_id": current_user.id,
            "type": "refresh"
        }, to=channel_name)

        # 2. To all users to update unread badges
        current_app.socketio.emit("message_created", {
            "channel": channel_name,
            "message_id": chat.id,
            "author_id": current_user.id
        })  # No 'to' means broadcast to everyone

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
        current_app.socketio.emit("chat_changed", {
            "channel": chat.channel.name,
            "message_id": chat.id,
            "author_id": current_user.id,
            "pinned": is_pinned
        }, to=chat.channel.name)
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
        
        # First delete all associated message states
        ChatMessageState.query.filter_by(message_id=chat_id).delete()
        
        # Then delete the message
        db.session.delete(chat)
        db.session.commit()

        current_app.socketio.emit("chat_changed", {"channel": channel_name}, room=channel_name)
        return "", 204
    except Exception as e:
        db.session.rollback()
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
