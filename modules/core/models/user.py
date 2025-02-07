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

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from system.db.database import db

class User(db.Model, UserMixin):
    """Core user model for authentication and basic user info"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_sample = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

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
    def create(cls, email, password, first_name=None, last_name=None, is_admin=False, is_sample=False):
        """Create new user"""
        if email == 'admin' and User.get_by_email('admin'):
            raise ValueError("Cannot create duplicate admin user")
        
        user = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user 

    def update_setting(self, key, value):
        """Update or create a user setting"""
        try:
            # Try to get existing setting
            setting = UserSetting.query.filter_by(
                user_id=self.id,
                key=key
            ).first()
            
            if setting:
                # Update existing setting
                setting.value = value
            else:
                # Create new setting
                setting = UserSetting(
                    user_id=self.id,
                    key=key,
                    value=value
                )
                db.session.add(setting)
                
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user setting: {str(e)}")
            return False
    
    
    
