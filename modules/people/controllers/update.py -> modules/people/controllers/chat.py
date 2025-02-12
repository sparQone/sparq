from ..models.chat import Chat
from ..models.chat import ChatType


@blueprint.route("/chat")
@login_required
def chat():
    """Company chat page"""
    return render_template(
        "chat/index.html",
        chat_types=ChatType,
        title="Company Chat",
        module_home="people_bp.people_home",
    )


@blueprint.route("/chat/create", methods=["POST"])
@login_required
def create_chat():
    try:
        chat_type = ChatType[request.form.get("type")]
        content = request.form.get("content")
        pinned = bool(request.form.get("pin"))

        chat = Chat(content=content, type=chat_type, author_id=current_user.id, pinned=pinned)
        db.session.add(chat)
        db.session.commit()

        # Emit WebSocket event
        socketio.emit("chat_changed")

        return ""
    except Exception as e:
        return str(e), 400
