from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ChatType(Enum):
    GENERAL = "General"
    ANNOUNCEMENT = "Announcement"
    EVENT = "Event"

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(ChatType), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pinned = db.Column(db.Boolean, default=False)
    # ... rest of the model definition 