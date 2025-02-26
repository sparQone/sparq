from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from datetime import datetime

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


@blueprint.route("/chat/messages/<int:message_id>")
@login_required
def get_single_message(message_id):
    """Get a single message by ID"""
    try:
        message = Chat.query.get_or_404(message_id)
        return render_template(
            "chat/partials/single-message.html",
            chat=message,
            current_user=current_user,
            ChatMessageState=ChatMessageState
        )
    except Exception as e:
        current_app.logger.error(f"Error getting message: {str(e)}")
        return str(e), 500


@blueprint.route("/chat/channels/<channel_name>/messages")
@login_required
def get_channel_messages(channel_name):
    """Get messages for a specific channel"""
    try:
        current_app.logger.info(f"Getting messages for channel {channel_name} for user {current_user.id}")
        
        # Get query parameters
        before_id = request.args.get('before_id', type=int)
        limit = request.args.get('limit', 10, type=int)
        pinned_only = request.args.get('pinned_only', type=bool)
        
        # Get channel
        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            return f"Channel {channel_name} not found", 404
            
        # Build base query
        query = channel.messages
        
        # Get total pin count for the channel
        total_pin_count = query.filter(Chat.pinned == True).count()
        
        # Filter pinned messages if requested
        if pinned_only:
            query = query.filter(Chat.pinned == True)
            
        # Get total count
        total_messages = query.count()
        if total_messages == 0:
            return render_template(
                "chat/partials/message-list.html",
                chats=[],
                current_user=current_user,
                channel_description=channel.description,
                ChatMessageState=ChatMessageState,
                has_more=False,
                oldest_id=None,
                channel_name=channel_name,
                total_pin_count=total_pin_count
            )
        
        # If before_id is not provided, get the latest messages
        if not before_id:
            messages = query.order_by(Chat.created_at.desc()).limit(limit).all()
            messages = messages[::-1]  # Reverse to show in ascending order
            has_more = query.filter(Chat.id < messages[0].id).first() is not None
            oldest_id = messages[0].id
        else:
            # Get messages before the given ID
            messages = query.filter(Chat.id < before_id).order_by(Chat.created_at.desc()).limit(limit).all()
            messages = messages[::-1]  # Reverse to show in ascending order
            has_more = query.filter(Chat.id < messages[0].id).first() is not None if messages else False
            oldest_id = messages[0].id if messages else None
            
        # Mark the entire channel as read
        # Get the latest message in the channel
        latest_message = Chat.query.filter_by(channel_id=channel.id).order_by(Chat.id.desc()).first()
        if latest_message:
            current_app.logger.info(f"Marking channel {channel_name} as read for user {current_user.id}")
            
            # Get or create a read state for this user and channel
            read_state = ChatMessageState.query.filter_by(
                user_id=current_user.id,
                channel_id=channel.id,
                interaction_type=InteractionType.READ
            ).first()
            
            if not read_state:
                current_app.logger.info(f"Creating new read state for channel {channel_name}")
                read_state = ChatMessageState(
                    user_id=current_user.id,
                    channel_id=channel.id,
                    message_id=latest_message.id,  # Associate with the latest message
                    interaction_type=InteractionType.READ,
                    data={'last_read_message_id': latest_message.id}
                )
                db.session.add(read_state)
            else:
                current_app.logger.info(f"Updating existing read state for channel {channel_name}")
                current_app.logger.info(f"Previous last read message ID: {read_state.data.get('last_read_message_id')}")
                # Don't change the message_id field to avoid unique constraint violation
                # read_state.message_id = latest_message.id  <- This line was causing the issue
                read_state.data = {'last_read_message_id': latest_message.id}
                read_state.updated_at = datetime.utcnow()
                
            db.session.commit()
            current_app.logger.info(f"Successfully marked channel {channel_name} as read")
        
        return render_template(
            "chat/partials/message-list.html",
            chats=messages,
            current_user=current_user,
            channel_description=channel.description,
            ChatMessageState=ChatMessageState,
            has_more=has_more,
            oldest_id=oldest_id,
            channel_name=channel_name,
            total_pin_count=total_pin_count
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
            return jsonify({"error": "Channel name is required"}), 400

        name = name.lower().replace(" ", "-")
        description = request.form.get("description")
        is_private = bool(request.form.get("is_private", False))

        # Check if channel already exists
        existing = Channel.query.filter_by(name=name).first()
        if existing:
            return jsonify({"error": "Channel already exists"}), 400

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
        return jsonify({"error": str(e)}), 400


@blueprint.route("/chat/messages", methods=["POST"])
@login_required
def create_message():
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


@blueprint.route("/chat/messages/<int:message_id>/pin", methods=["POST"])
@login_required
def toggle_pin(message_id):
    """Toggle pin status of a message"""
    try:
        chat = Chat.query.get_or_404(message_id)
        if not current_user.is_admin and not chat.is_author:
            return jsonify({"error": "Unauthorized"}), 403

        chat.toggle_pin()
        
        # Get updated pin count for the channel
        total_pin_count = Chat.query.filter_by(channel_id=chat.channel_id, pinned=True).count()
        
        db.session.commit()
        
        return render_template(
            "chat/partials/single-message.html",
            chat=chat,
            current_user=current_user,
            ChatMessageState=ChatMessageState,
            total_pin_count=total_pin_count
        )
    except Exception as e:
        return str(e), 400


@blueprint.route("/chat/messages/<int:message_id>", methods=["DELETE"])
@login_required
def delete_message(message_id):
    """Delete a chat message"""
    try:
        chat = Chat.query.get_or_404(message_id)
        if not current_user.is_admin and not chat.is_author:
            return jsonify({"error": "Unauthorized"}), 403

        channel_name = chat.channel.name
        
        # First delete all associated message states
        ChatMessageState.query.filter_by(message_id=message_id).delete()
        
        # Then delete the message
        db.session.delete(chat)
        db.session.commit()

        current_app.socketio.emit("chat_changed", {"channel": channel_name}, room=channel_name)
        return "", 204
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting message: {str(e)}")
        return jsonify({"error": str(e)}), 400


@blueprint.route("/chat/channels/<channel_name>", methods=["DELETE"])
@login_required
def delete_channel(channel_name):
    """Delete a channel"""
    try:
        if not current_user.is_admin:
            return jsonify({"error": "Unauthorized"}), 403

        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            return jsonify({"error": "Channel not found"}), 404

        # Don't allow deleting default channels
        if channel.name in ["general", "announcements", "events"]:
            return jsonify({"error": "Cannot delete default channels"}), 400

        # Delete all message states for this channel
        ChatMessageState.query.filter_by(channel_id=channel.id).delete()
        
        # Delete all messages in this channel
        Chat.query.filter_by(channel_id=channel.id).delete()
        
        # Delete the channel
        db.session.delete(channel)
        db.session.commit()

        current_app.socketio.emit("channel_deleted", {"name": channel_name})
        return "", 204
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting channel: {str(e)}")
        return jsonify({"error": str(e)}), 400


@blueprint.route("/chat/channels/edit", methods=["PUT"])
@login_required
def edit_channel():
    """Edit a channel"""
    try:
        if not current_user.is_admin:
            return jsonify({"error": "Unauthorized"}), 403

        original_channel_name = request.form.get("original_channel_name")
        new_channel_name = request.form.get("channel_name")
        description = request.form.get("description")
        
        if not original_channel_name or not new_channel_name:
            return jsonify({"error": "Channel name is required"}), 400

        # Check if original channel exists
        channel = Channel.query.filter_by(name=original_channel_name).first()
        if not channel:
            return jsonify({"error": "Channel not found"}), 404

        # Don't allow editing default channels
        if channel.name in ["general", "announcements", "events"]:
            return jsonify({"error": "Cannot edit default channels"}), 400
            
        # If channel name is changing, check if the new name already exists
        if original_channel_name != new_channel_name:
            existing_channel = Channel.query.filter_by(name=new_channel_name).first()
            if existing_channel:
                return jsonify({"error": "A channel with this name already exists"}), 400
                
            # Update channel name
            channel.name = new_channel_name

        # Update channel description
        channel.description = description
        db.session.commit()

        return jsonify({"name": channel.name, "description": channel.description})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error editing channel: {str(e)}")
        return jsonify({"error": str(e)}), 400


@blueprint.route("/chat/channels/<channel_name>/search", methods=["POST"])
@login_required
def search_channel_messages(channel_name):
    """Search messages in a channel"""
    try:
        search_term = request.form.get('search', '').strip()
        
        # Get channel
        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            return f"Channel {channel_name} not found", 404
            
        # Build search query
        query = channel.messages
        
        # If search term exists, filter messages
        if search_term:
            search_term = f"%{search_term}%"
            query = query.filter(
                db.or_(
                    Chat.content.ilike(search_term),
                    db.and_(
                        Chat.author_id == User.id,
                        db.or_(
                            User.first_name.ilike(search_term),
                            User.last_name.ilike(search_term)
                        )
                    )
                )
            ).order_by(Chat.created_at.desc())
            messages = query.all()
            messages = messages[::-1]  # Reverse to show in ascending order
            has_more = False  # Don't show load more button in search results
            oldest_id = None
        else:
            # If no search term, return recent messages
            messages = query.order_by(Chat.created_at.desc()).limit(10).all()
            messages = messages[::-1]  # Reverse to show in ascending order
            has_more = query.filter(Chat.id < messages[0].id).first() is not None if messages else False
            oldest_id = messages[0].id if messages else None
        
        # Get total pin count for the channel
        total_pin_count = Chat.query.filter_by(channel_id=channel.id, pinned=True).count()
        
        return render_template(
            "chat/partials/message-list.html",
            chats=messages,
            current_user=current_user,
            channel_description=channel.description,
            ChatMessageState=ChatMessageState,
            has_more=has_more,
            oldest_id=oldest_id,
            channel_name=channel_name,
            total_pin_count=total_pin_count
        )
            
    except Exception as e:
        current_app.logger.error(f"Error searching messages: {str(e)}")
        return str(e), 500


@blueprint.route("/chat/channels/unread")
@login_required
def get_unread_channels():
    """Get unread status for all channels"""
    try:
        channels = Channel.query.all()
        unread_status = {}
        
        # Debug information
        current_app.logger.info(f"Getting unread status for user {current_user.id}")
        
        for channel in channels:
            # Check if there are any messages in the channel
            message_count = Chat.query.filter_by(channel_id=channel.id).count()
            
            if message_count == 0:
                # No messages in the channel, so it can't be unread
                unread_status[channel.name] = False
                current_app.logger.info(f"Channel {channel.name} has no messages, marking as read")
                continue
                
            # Get the latest message in the channel
            latest_message = Chat.query.filter_by(channel_id=channel.id).order_by(Chat.id.desc()).first()
            
            # Get the last read state for this user and channel
            last_read = ChatMessageState.query.filter_by(
                user_id=current_user.id,
                channel_id=channel.id,
                interaction_type=InteractionType.READ
            ).order_by(ChatMessageState.updated_at.desc()).first()
            
            # If no read state exists, the channel has unread messages
            if not last_read or not last_read.data:
                unread_status[channel.name] = True
                current_app.logger.info(f"Channel {channel.name} has no read state, marking as unread")
                continue
                
            # Get the ID of the last read message
            last_read_id = last_read.data.get('last_read_message_id')
            if last_read_id is None:
                unread_status[channel.name] = True
                current_app.logger.info(f"Channel {channel.name} has no last read message ID, marking as unread")
                continue
                
            # Check if the latest message is newer than the last read message
            has_unread = latest_message.id > last_read_id
            unread_status[channel.name] = has_unread
            current_app.logger.info(f"Channel {channel.name} unread status: {has_unread} (latest: {latest_message.id}, last read: {last_read_id})")
            
        return jsonify(unread_status)
    except Exception as e:
        current_app.logger.error(f"Error getting unread channels: {str(e)}")
        current_app.logger.exception(e)
        return jsonify({}), 500


@blueprint.route("/chat/channels/<channel_name>/mark_read", methods=["POST"])
@login_required
def mark_channel_read_endpoint(channel_name):
    """Mark a channel as read for the current user"""
    try:
        current_app.logger.info(f"Marking channel {channel_name} as read for user {current_user.id}")
        
        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            current_app.logger.error(f"Channel {channel_name} not found")
            return jsonify({"error": f"Channel {channel_name} not found"}), 404
            
        # Get the latest message in the channel
        latest_message = Chat.query.filter_by(channel_id=channel.id).order_by(Chat.id.desc()).first()
        if not latest_message:
            current_app.logger.info(f"No messages in channel {channel_name}, nothing to mark as read")
            return jsonify({"status": "success", "message": "No messages to mark as read"})
            
        current_app.logger.info(f"Latest message ID in channel {channel_name}: {latest_message.id}")
            
        # Get or create a read state for this user and channel
        read_state = ChatMessageState.query.filter_by(
            user_id=current_user.id,
            channel_id=channel.id,
            interaction_type=InteractionType.READ
        ).first()
        
        if not read_state:
            current_app.logger.info(f"Creating new read state for channel {channel_name}")
            read_state = ChatMessageState(
                user_id=current_user.id,
                channel_id=channel.id,
                message_id=latest_message.id,  # Associate with the latest message
                interaction_type=InteractionType.READ,
                data={'last_read_message_id': latest_message.id}
            )
            db.session.add(read_state)
        else:
            current_app.logger.info(f"Updating existing read state for channel {channel_name}")
            current_app.logger.info(f"Previous last read message ID: {read_state.data.get('last_read_message_id')}")
            # Don't change the message_id field to avoid unique constraint violation
            # read_state.message_id = latest_message.id  <- This line was causing the issue
            read_state.data = {'last_read_message_id': latest_message.id}
            read_state.updated_at = datetime.utcnow()
            
        db.session.commit()
        current_app.logger.info(f"Successfully marked channel {channel_name} as read")
        
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error marking channel as read: {str(e)}")
        current_app.logger.exception(e)
        return jsonify({"error": str(e)}), 500


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
