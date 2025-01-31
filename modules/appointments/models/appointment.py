# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Appointment model that handles scheduling data and relationships.
#     Provides core appointment booking and calendar management functionality.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from system.db.database import db
from datetime import datetime
from enum import Enum

class AppointmentStatus(Enum):
    SCHEDULED = 'scheduled'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

class Appointment(db.Model):
    """Appointment model for scheduling system"""
    __tablename__ = 'appointment'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    notes = db.Column(db.Text)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='appointments') 