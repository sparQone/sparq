from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from datetime import datetime
from system.db.database import db
from system.db.decorators import ModelRegistry
from .associations import chat_likes

class ChatType(Enum):
    GENERAL = "General"
    ANNOUNCEMENT = "Announcement"
    EVENT = "Event"

@ModelRegistry.register
class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(ChatType), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pinned = db.Column(db.Boolean, default=False)
    
    # Define relationships with backrefs here
    author = db.relationship('User', 
                           foreign_keys=[author_id],
                           backref=db.backref('authored_chats', lazy='dynamic'),
                           lazy='joined')
    liked_by = db.relationship('User', 
                               secondary=chat_likes,
                               backref=db.backref('liked_messages', lazy='dynamic'),
                               lazy='dynamic')
    
    @property
    def created_at_formatted(self):
        """Format the creation date for display"""
        return self.created_at.strftime("%B %d, %Y %I:%M %p")
    
    @property
    def is_author(self):
        """Check if current user is the author"""
        return current_user.is_authenticated and self.author_id == current_user.id
    
    @property
    def is_liked(self):
        """Check if current user has liked this chat"""
        return current_user.is_authenticated and current_user in self.liked_by

    def toggle_pin(self):
        """Toggle pinned status"""
        self.pinned = not self.pinned
        db.session.commit()
        return self.pinned 