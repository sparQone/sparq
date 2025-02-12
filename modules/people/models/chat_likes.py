from system.db.database import db

# Create the chat_likes association table
chat_likes = db.Table(
    "chat_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("chat_id", db.Integer, db.ForeignKey("chat.id"), primary_key=True),
)
