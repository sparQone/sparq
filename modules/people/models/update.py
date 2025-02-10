# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module models for update functionality.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.

from datetime import datetime
from enum import Enum
from flask import current_app

from system.db.database import db
from system.db.decorators import ModelRegistry
from system.i18n.translation import translate as _

class UpdateType(Enum):
    # Store untranslated strings as values
    GENERAL = "General"
    ANNOUNCEMENT = "Announcement"
    NEWS = "News"
    EVENT = "Event"

    def __str__(self):
        # Translate the value when the enum is displayed
        return _(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    @property
    def translated(self):
        # Convenience property to get translated value
        return _(self.value)


@ModelRegistry.register
class Reply(db.Model):
    """Update reply model"""

    __tablename__ = "update_reply"

    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey("update.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Use backref instead of back_populates
    update = db.relationship("Update", backref="replies")
    user = db.relationship("User", backref="update_replies")


@ModelRegistry.register
class Update(db.Model):
    """Update model"""

    __tablename__ = "update"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.Enum(UpdateType), nullable=False, default=UpdateType.GENERAL)
    content = db.Column(db.Text, nullable=False)
    pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Use backref instead of back_populates
    user = db.relationship("User", backref="updates")
    likes = db.relationship("User", secondary="update_like", backref=db.backref("liked_updates"))


# Association table for likes
update_like = db.Table(
    "update_like",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("update_id", db.Integer, db.ForeignKey("update.id"), primary_key=True),
    db.Column("created_at", db.DateTime, default=datetime.utcnow),
)
