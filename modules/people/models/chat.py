# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Chat and Channel models for the team communication system.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------


from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from datetime import datetime
from system.db.database import db
from system.db.decorators import ModelRegistry
from .associations import chat_likes
from flask import current_app
from markupsafe import Markup
import re
from typing import Optional, List

@ModelRegistry.register
class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now())
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_private = db.Column(db.Boolean, default=False)
    
    # Relationships
    created_by = db.relationship('User', foreign_keys=[created_by_id])
    messages = db.relationship('Chat', backref='channel', lazy='dynamic')

    def __init__(self, name, description=None, created_by_id=None, is_private=False):
        self.name = name
        self.description = description
        self.created_by_id = created_by_id
        self.is_private = is_private

    @classmethod
    def create_default_channels(cls):
        """Create default channels if they don't exist"""
        default_channels = [
            {
                'name': 'general',
                'description': 'General discussion channel'
            },
            {
                'name': 'announcements',
                'description': 'Important company announcements'
            },
            {
                'name': 'events',
                'description': 'Company events and activities'
            }
        ]

        for channel_data in default_channels:
            channel = cls.query.filter_by(name=channel_data['name']).first()
            if not channel:
                channel = cls(
                    name=channel_data['name'],
                    description=channel_data['description']
                )
                db.session.add(channel)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating default channels: {str(e)}")

@ModelRegistry.register
class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
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
    def created_at_formatted(self) -> str:
        """Format the creation date for display"""
        return self.created_at.strftime("%B %d, %Y %I:%M %p")
    
    @property
    def is_author(self) -> bool:
        """Check if current user is the author"""
        return current_user.is_authenticated and self.author_id == current_user.id
    
    @property
    def is_liked(self) -> bool:
        """Check if current user has liked this chat"""
        return current_user.is_authenticated and current_user in self.liked_by

    def toggle_pin(self) -> bool:
        """Toggle pinned status"""
        self.pinned = not self.pinned
        db.session.commit()
        return self.pinned

    @property
    def formatted_content(self) -> Markup:
        """Format message content with clickable links"""
        url_pattern = r'(https?://[^\s<>"]+|www\.[^\s<>"]+)'
        
        def replace_url(match):
            url = match.group(0)
            display_url = url[:50] + '...' if len(url) > 50 else url
            full_url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
            return f'<a href="{full_url}" target="_blank" rel="noopener noreferrer" class="chat-link">{display_url}</a>'
        
        content = re.sub(url_pattern, replace_url, self.content)
        content = content.replace('\n', '<br>')
        
        return Markup(content) 