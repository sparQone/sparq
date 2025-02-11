# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Core user model that handles authentication, user management, and
#     provides base user functionality for the entire application. Implements
#     Flask-Login integration and password hashing.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

import logging
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from system.db.database import db
from system.db.decorators import ModelRegistry
from modules.core.models.group import Group
from modules.core.models.user_group import user_group

logger = logging.getLogger(__name__)

@ModelRegistry.register
class User(db.Model, UserMixin):
    """Core user model for authentication and basic user info"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    is_sample = db.Column(db.Boolean, default=False)

    # One-to-one relationship with Employee
    employee_profile = db.relationship('Employee', backref=db.backref('user', uselist=False), uselist=False)

    # Update the relationship to use the imported table
    groups = db.relationship('Group', secondary=user_group, backref=db.backref('users', lazy='dynamic'))

    @property
    def is_admin(self):
        """Check if user is in ADMIN group"""
        return any(group.name == "ADMIN" for group in self.groups)

    @property
    def is_sole_admin(self):
        """Check if user is the only administrator"""
        if not self.is_admin:
            return False
        
        admin_count = User.query.filter(
            User.groups.any(name="ADMIN")
        ).count()
        return admin_count <= 1

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return User.query.get(int(user_id))

    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()

    @classmethod
    def create(cls, email, password, first_name=None, last_name=None, is_admin=False):
        """Create new user and add to appropriate groups"""
        # Check for duplicate admin
        if email == "admin" and User.get_by_email("admin"):
            raise ValueError("Cannot create duplicate admin user")
        
        # Create new user instance
        user = cls(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.password = password  # This will hash the password
        db.session.add(user)
        
        # Add to ALL group
        all_group = Group.get_or_create("ALL", "Default group for all users", True)
        user.add_to_group(all_group)
        
        # Add to ADMIN group if specified
        if is_admin:
            admin_group = Group.get_or_create("ADMIN", "Administrators group", True)
            user.add_to_group(admin_group)
        
        db.session.commit()
        return user

    def update_setting(self, key, value):
        """Update or create a user setting"""
        try:
            # Try to get existing setting
            setting = UserSetting.query.filter_by(user_id=self.id, key=key).first()

            if setting:
                # Update existing setting
                setting.value = value
            else:
                # Create new setting
                setting = UserSetting(user_id=self.id, key=key, value=value)
                db.session.add(setting)

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error updating user setting: {str(e)}")
            return False

    def add_to_group(self, group):
        """Add user to group if not already member"""
        if group not in self.groups:
            self.groups.append(group)
            db.session.commit()
    
    def remove_from_group(self, group):
        """Remove user from group if not ALL group"""
        if group.name != "ALL" and group in self.groups:
            # Prevent removing last admin
            if group.name == "ADMIN":
                admin_count = User.query.filter(
                    User.groups.any(name="ADMIN")
                ).count()
                if admin_count <= 1 and self.is_admin:
                    raise ValueError("Cannot remove last admin user")
            
            self.groups.remove(group)
            db.session.commit()
