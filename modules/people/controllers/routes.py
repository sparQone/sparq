# from . import blueprint

# @blueprint.route("/chat")
# @login_required
# def chat():
#     """Company chat page"""
#     chats = Chat.query.order_by(Chat.pinned.desc(), Chat.created_at.desc()).all()
#     return render_template("chat/index.html",
#                         active_page='chat',
#                         title="Company Chat",
#                         chat_types=ChatType,
#                         chats=chats,
#                         module_home='people_bp.people_home')
# 
# @blueprint.route("/chat/create", methods=["POST"])
# @login_required
# def create_chat():
#     """Create a new chat message"""
#     try:
#         chat_type = ChatType[request.form.get("type")]
#         content = request.form.get("content")
#         pinned = bool(request.form.get("pin"))
# 
#         chat = Chat(
#             content=content,
#             type=chat_type,
#             author_id=current_user.id,
#             pinned=pinned
#         )
#         db.session.add(chat)
#         db.session.commit()
# 
#         # Emit WebSocket event
#         socketio.emit("chat_changed")
#         
#         return ""
#     except Exception as e:
#         return str(e), 400 