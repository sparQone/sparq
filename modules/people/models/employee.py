# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Employee model that handles employee data management and relationships.
#     Provides core employee information storage and retrieval functionality.
#
# Copyright (c) 2025 remarQable LLC
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

    hire_date = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, email, password=None, first_name=None, last_name=None, is_admin=False, **kwargs):
        """
        Create new employee profile, creating user if needed
        
        Args:
            email (str): User email
            password (str, optional): User password. Random if not provided
            first_name (str, optional): User first name
            last_name (str, optional): User last name
            is_admin (bool, optional): Whether user is admin
            **kwargs: Additional employee fields (department, position, type, etc)
        
        Returns:
            Employee: Created employee instance
        """
        try:
            # Check if user exists
            user = User.get_by_email(email)
            
            # Create user if doesn't exist
            if not user:
                user = User.create(
                    email=email,
                    password=password or User.generate_random_password(),
                    first_name=first_name,
                    last_name=last_name,
                    is_admin=is_admin
                )
            
            # Create employee profile
            employee = cls(
                user=user,
                department=kwargs.get('department', ''),
                position=kwargs.get('position', ''),
                type=EmployeeType[kwargs.get('type', 'FULL_TIME')],
                status=kwargs.get('status', EmployeeStatus.ACTIVE),
                start_date=kwargs.get('start_date', datetime.utcnow().date())
            )
            
            db.session.add(employee)
            db.session.commit()
            return employee
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def get_by_email(cls, email):
        """Get employee by email"""
        return cls.query.join(User).filter(User.email == email).first()
    
    @classmethod
    def create_sample_employees(cls):
        """Create sample employees for testing/demo purposes"""
        sample_employees = [    
            {
                'email': 'sarah@allaboutpies.shop',
                'password': 'password123',
                'first_name': 'Sarah',
                'last_name': 'Smith',
                'is_admin': True,
                'department': 'Management',
                'position': 'CEO',
                'type': 'FULL_TIME'
            },
            {
                'email': 'michael@allaboutpies.shop', 
                'password': 'password123',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'department': 'Kitchen',
                'position': 'Head Chef',
                'type': 'FULL_TIME'
            },
            {
                'email': 'david@allaboutpies.shop',
                'password': 'password123', 
                'first_name': 'David',
                'last_name': 'Smith',
                'department': 'Service',
                'position': 'Server',
                'type': 'PART_TIME'
            }
        ]

        for employee_data in sample_employees:
            if not cls.get_by_email(employee_data['email']):
                cls.create(**employee_data)