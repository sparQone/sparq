# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Employee model that handles employee data management and relationships.
#     Provides core employee information storage and retrieval functionality.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from system.db.database import db
from enum import Enum
from modules.core.models.user import User
from datetime import datetime

class EmployeeStatus(Enum):
    ACTIVE = 'active'
    ON_LEAVE = 'on_leave'
    TERMINATED = 'terminated'
    CONTRACTOR = 'contractor'

class EmployeeType(Enum):
    FULL_TIME = 'full_time'
    PART_TIME = 'part_time'
    CONTRACTOR = 'contractor'
    INTERN = 'intern'

def generate_employee_id():
    """Generate unique employee ID"""
    # You can implement your company's employee ID generation logic here
    import random
    return f"EMP{random.randint(10000, 99999)}"

class Employee(db.Model):
    """Employee specific information"""
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    
    # Employee specific fields
    employee_id = db.Column(db.String(20), unique=True, default=generate_employee_id)
    department = db.Column(db.String(50))
    position = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    status = db.Column(db.Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    type = db.Column(db.Enum(EmployeeType), default=EmployeeType.FULL_TIME)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('employee_profile', uselist=False))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    reports = db.relationship('Employee', backref=db.backref('manager', remote_side=[id]))

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user, **kwargs):
        """Create new employee profile"""
        employee = cls(user=user, **kwargs)
        db.session.add(employee)
        db.session.commit()
        return employee 