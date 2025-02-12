from system.db.database import db
from system.db.decorators import ModelRegistry

# Association tables for relationships
chat_like = db.Table(
    "chat_like",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("chat_id", db.Integer, db.ForeignKey("chat.id"), primary_key=True),
)

# Register the association table
ModelRegistry.register_table(chat_like, "people")
