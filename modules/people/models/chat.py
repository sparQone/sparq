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


import re
from enum import Enum
from datetime import datetime

from flask import current_app
from flask_login import current_user
from markupsafe import Markup

from system.db.database import db
from system.db.decorators import ModelRegistry

from .associations import chat_like


@ModelRegistry.register
class Channel(db.Model):
    __tablename__ = "channel"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now())
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_private = db.Column(db.Boolean, default=False)

    # Relationships
    created_by = db.relationship("User", foreign_keys=[created_by_id])
    messages = db.relationship("Chat", backref="channel", lazy="dynamic")

    def __init__(self, name, description=None, created_by_id=None, is_private=False):
        self.name = name
        self.description = description
        self.created_by_id = created_by_id
        self.is_private = is_private

    @classmethod
    def create_default_channels(cls):
        """Create default channels if they don't exist"""
        default_channels = [
            {"name": "general", "description": "General discussion channel"},
            {"name": "announcements", "description": "Important company announcements"},
            {"name": "events", "description": "Company events and activities"},
        ]

        for channel_data in default_channels:
            channel = cls.query.filter_by(name=channel_data["name"]).first()
            if not channel:
                channel = cls(name=channel_data["name"], description=channel_data["description"])
                db.session.add(channel)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating default channels: {str(e)}")


@ModelRegistry.register
class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    pinned = db.Column(db.Boolean, default=False)

    # Define relationships with backrefs here
    author = db.relationship(
        "User",
        foreign_keys=[author_id],
        backref=db.backref("authored_chats", lazy="dynamic"),
        lazy="joined",
    )
    liked_by = db.relationship(
        "User",
        secondary=chat_like,
        backref=db.backref("liked_messages", lazy="dynamic"),
        lazy="dynamic",
    )

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
            display_url = url[:50] + "..." if len(url) > 50 else url
            full_url = url if url.startswith(("http://", "https://")) else f"https://{url}"
            return f'<a href="{full_url}" target="_blank" rel="noopener noreferrer" class="chat-link">{display_url}</a>'

        content = re.sub(url_pattern, replace_url, self.content)
        content = content.replace("\n", "<br>")

        return Markup(content)


class InteractionType(Enum):
    READ = "read"              # Track read status
    REACTION = "reaction"      # For emoji reactions
    BOOKMARK = "bookmark"      # For saving messages
    THREAD_READ = "thread_read"  # For thread read status
    PIN = "pin"               # For pinning messages
    LIKE = "like"             # For liking messages
    EDIT = "edit"             # Track edit history
    DELETE = "delete"         # Soft deletes


@ModelRegistry.register
class ChatMessageState(db.Model):
    """
    Generic model to track user interactions with messages.
    This model can handle multiple types of interactions and states.
    """
    __tablename__ = 'chat_message_state'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    interaction_type = db.Column(db.Enum(InteractionType), nullable=False)
    
    # Flexible data storage for different interaction types
    data = db.Column(db.JSON, nullable=True)  # Store interaction-specific data
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    __table_args__ = (
        db.UniqueConstraint('user_id', 'message_id', 'interaction_type', 
                          name='unique_user_message_interaction'),
    )

    # Relationships
    user = db.relationship('User', backref=db.backref('chat_message_states', lazy='dynamic'))
    message = db.relationship('Chat', backref=db.backref('states', lazy='dynamic'))
    channel = db.relationship('Channel', backref=db.backref('message_states', lazy='dynamic'))

    @classmethod
    def get_unread_count(cls, user_id, channel_id):
        """Get number of unread messages in a channel for a user"""
        try:
            last_read = cls.query.filter_by(
                user_id=user_id,
                channel_id=channel_id,
                interaction_type=InteractionType.READ
            ).order_by(cls.updated_at.desc()).first()
            
            if not last_read or not last_read.data:
                return Chat.query.filter_by(channel_id=channel_id).count()
            
            last_read_id = last_read.data.get('last_read_message_id')
            if last_read_id is None:
                return Chat.query.filter_by(channel_id=channel_id).count()
            
            return Chat.query.filter(
                Chat.channel_id == channel_id,
                Chat.id > last_read_id
            ).count()
        except Exception as e:
            current_app.logger.error(f"Error getting unread count: {str(e)}")
            current_app.logger.exception(e)
            return 0  # Return 0 on error to avoid breaking the UI

    @classmethod
    def has_unread(cls, user_id, channel_id):
        """Check if a channel has any unread messages for a user"""
        try:
            channel = Channel.query.get(channel_id)
            current_app.logger.debug(f"Checking unread status for channel {channel.name} (ID: {channel_id}) for user {user_id}")
            
            # First check if there are any messages in the channel
            message_count = Chat.query.filter_by(channel_id=channel_id).count()
            current_app.logger.debug(f"Channel {channel.name} has {message_count} messages")
            
            if message_count == 0:
                current_app.logger.debug(f"Channel {channel.name} has no messages, returning False")
                return False
                
            # Get the latest message in the channel
            latest_message = Chat.query.filter_by(channel_id=channel_id).order_by(Chat.id.desc()).first()
            current_app.logger.debug(f"Latest message ID in channel {channel.name}: {latest_message.id}")
            
            # Get the last read state for this user and channel
            last_read = cls.query.filter_by(
                user_id=user_id,
                channel_id=channel_id,
                interaction_type=InteractionType.READ
            ).order_by(cls.updated_at.desc()).first()
            
            # If no read state exists, the channel has unread messages
            if not last_read:
                current_app.logger.debug(f"No read state exists for channel {channel.name}, returning True")
                return True
                
            if not last_read.data:
                current_app.logger.debug(f"Read state exists but has no data for channel {channel.name}, returning True")
                return True
            
            # Get the ID of the last read message
            last_read_id = last_read.data.get('last_read_message_id')
            current_app.logger.debug(f"Last read message ID for channel {channel.name}: {last_read_id}")
            
            if last_read_id is None:
                current_app.logger.debug(f"Last read message ID is None for channel {channel.name}, returning True")
                return True
            
            # Check if the latest message is newer than the last read message
            result = latest_message.id > last_read_id
            current_app.logger.debug(f"Channel {channel.name} has unread messages: {result} (latest: {latest_message.id}, last read: {last_read_id})")
            return result
        except Exception as e:
            current_app.logger.error(f"Error checking for unread messages: {str(e)}")
            current_app.logger.exception(e)
            return False  # Return False on error to avoid breaking the UI

    @classmethod
    def mark_channel_read(cls, user_id, channel_id):
        """Mark all messages in a channel as read for a user"""
        try:
            channel = Channel.query.get(channel_id)
            current_app.logger.debug(f"Marking channel {channel.name} (ID: {channel_id}) as read for user {user_id}")
            
            # Get the latest message in the channel
            latest_message = Chat.query.filter_by(channel_id=channel_id).order_by(Chat.id.desc()).first()
            if not latest_message:
                current_app.logger.debug(f"No messages in channel {channel.name}, nothing to mark as read")
                return True  # No messages to mark as read
                
            current_app.logger.debug(f"Latest message ID in channel {channel.name}: {latest_message.id}")
                
            # Get or create a read state for this user and channel
            read_state = cls.query.filter_by(
                user_id=user_id,
                channel_id=channel_id,
                interaction_type=InteractionType.READ
            ).first()
            
            if not read_state:
                current_app.logger.debug(f"Creating new read state for channel {channel.name}")
                read_state = cls(
                    user_id=user_id,
                    channel_id=channel_id,
                    message_id=latest_message.id,  # Associate with the latest message
                    interaction_type=InteractionType.READ,
                    data={'last_read_message_id': latest_message.id}
                )
                db.session.add(read_state)
            else:
                current_app.logger.debug(f"Updating existing read state for channel {channel.name}")
                current_app.logger.debug(f"Previous last read message ID: {read_state.data.get('last_read_message_id')}")
                # Don't change the message_id field to avoid unique constraint violation
                # read_state.message_id = latest_message.id  <- This line was causing the issue
                read_state.data = {'last_read_message_id': latest_message.id}
                read_state.updated_at = datetime.utcnow()
                
            db.session.commit()
            current_app.logger.debug(f"Successfully marked channel {channel.name} as read")
            return True
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error marking channel as read: {str(e)}")
            current_app.logger.exception(e)
            return False

    @classmethod
    def mark_message_read(cls, user_id, message_id):
        """Mark a specific message as read for a user"""
        try:
            # Get the message to get its channel_id
            message = Chat.query.get(message_id)
            if not message:
                return False

            # Check if we already have a read state for this user/message/type
            existing = cls.query.filter_by(
                user_id=user_id,
                message_id=message_id,
                channel_id=message.channel_id,
                interaction_type=InteractionType.READ
            ).first()

            if existing:
                # Update existing record
                existing.data = {'last_read_message_id': message_id}
                existing.updated_at = db.func.now()
            else:
                # Create new record
                state = cls(
                    user_id=user_id,
                    message_id=message_id,
                    channel_id=message.channel_id,
                    interaction_type=InteractionType.READ,
                    data={'last_read_message_id': message_id}
                )
                db.session.add(state)

            return True
        except Exception as e:
            current_app.logger.error(f"Error marking message as read: {str(e)}")
            current_app.logger.exception(e)
            return False
