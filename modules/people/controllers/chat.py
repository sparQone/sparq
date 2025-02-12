from flask import current_app, jsonify, render_template, request
from flask_login import current_user, login_required
from flask_socketio import SocketIO
from system.db.database import db
from system.i18n.translation import _
from ..models.chat import Chat, ChatType
from . import blueprint

@blueprint.route("/chat")
@login_required
def chat():
    """Company chat page"""
    chats = Chat.query.order_by(Chat.pinned.desc(), Chat.created_at.desc()).all()
    return render_template(
        "chat/index.html",
        active_page='chat',
        title="Company Chat",
        chat_types=ChatType,
        chats=chats,
        module_home="people_bp.people_home",
    )

@blueprint.route("/chat/list")
@login_required
def get_chats():
    """Get chat list for HTMX updates"""
    try:
        chats = Chat.query.order_by(Chat.pinned.desc(), Chat.created_at.desc()).all()
        return render_template(
            "chat/partials/chat_list.html",
            chats=chats,
            current_user=current_user
        )
    except Exception as e:
        current_app.logger.error(f"Error getting chat list: {str(e)}")
        return str(e), 500

@blueprint.route("/chat/create", methods=["POST"])
@login_required
def create_chat():
    """Create a new chat message"""
    try:
        # Get form data with defaults
        chat_type = request.form.get("type", "GENERAL")
        if isinstance(chat_type, str):
            chat_type = ChatType[chat_type.upper()]
        content = request.form.get("content")
        pinned = bool(request.form.get("pin", False))

        # Validate required fields
        if not content:
            return "Content is required", 400

        chat = Chat(
            content=content,
            type=chat_type,
            author_id=current_user.id,
            pinned=pinned
        )
        db.session.add(chat)
        db.session.commit()

        # Emit WebSocket event
        current_app.socketio.emit("chat_changed")
        
        return ""
    except KeyError as e:
        return f"Invalid chat type: {str(e)}", 400
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
        current_app.socketio.emit("chat_changed")
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
        
        db.session.delete(chat)
        db.session.commit()
        current_app.socketio.emit("chat_changed")
        return "", 204
    except Exception as e:
        return jsonify({"error": str(e)}), 400 