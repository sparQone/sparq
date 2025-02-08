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
from system.db.decorators import ModelRegistry

class EmployeeStatus(Enum):
    ACTIVE = 'Active'
    ON_LEAVE = 'On Leave'
    TERMINATED = 'Terminated'
    CONTRACTOR = 'Contractor'

class EmployeeType(Enum):
    FULL_TIME = 'Full Time'
    PART_TIME = 'Part Time'
    CONTRACTOR = 'Contractor'
    INTERN = 'Intern'

class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    PREFER_NOT_TO_SAY = 'Prefer not to say'

def generate_employee_id():
    """Generate unique employee ID"""
    import random
    return f"EMP{random.randint(10000, 99999)}"

@ModelRegistry.register
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
    
    # New fields for personal information
    phone = db.Column(db.String(20))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(50))
    salary = db.Column(db.Numeric(10, 2))  # Allows for decimal places
    
    # Personal information
    birthday = db.Column(db.Date)
    gender = db.Column(db.Enum(Gender))
    
    # Emergency contact
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    
    # Social media
    social_media = db.Column(db.String(100))
    
    # Existing relationships
    user = db.relationship('User', backref=db.backref('employee_profile', uselist=False))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    reports = db.relationship('Employee', backref=db.backref('manager', remote_side=[id]))
    

    @property
    def full_address(self):
        """Return formatted full address"""
        parts = [self.address, self.city, self.state, self.zip_code, self.country]
        return ', '.join(filter(None, parts))

    @property
    def formatted_salary(self):
        """Return formatted salary with currency"""
        if self.salary:
            return f"${self.salary:,.2f}/Yearly"
        return None

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
            **kwargs: Additional employee fields
        
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
            
            # Create employee profile with all possible fields
            employee = cls(
                user=user,
                department=kwargs.get('department', ''),
                position=kwargs.get('position', ''),
                type=EmployeeType[kwargs.get('type', 'FULL_TIME')],
                status=kwargs.get('status', EmployeeStatus.ACTIVE),
                start_date=kwargs.get('start_date', datetime.utcnow().date()),
                # New fields
                phone=kwargs.get('phone', ''),
                address=kwargs.get('address', ''),
                city=kwargs.get('city', ''),
                state=kwargs.get('state', ''),
                zip_code=kwargs.get('zip_code', ''),
                country=kwargs.get('country', ''),
                salary=kwargs.get('salary'),
                birthday=kwargs.get('birthday'),
                gender=Gender[kwargs.get('gender')] if kwargs.get('gender') else None,
                emergency_contact_name=kwargs.get('emergency_contact_name', ''),
                emergency_contact_phone=kwargs.get('emergency_contact_phone', ''),
                emergency_contact_relationship=kwargs.get('emergency_contact_relationship', ''),
                social_media=kwargs.get('social_media', '')
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
                'last_name': 'Baker',  # Changed to match the UI
                'is_admin': True,
                'department': 'Management',
                'position': 'Owner',  # Changed to match the UI
                'type': 'FULL_TIME',
                # Personal information
                'phone': '612-456-7890',
                'address': '100 Main St',
                'city': 'Minneapolis',
                'state': 'MN',
                'zip_code': '55401',
                'country': 'USA',
                'salary': 90000.00,
                'birthday': datetime(1980, 1, 1).date(),
                'gender': 'FEMALE',
                # Emergency contact
                'emergency_contact_name': 'Jill Baker',
                'emergency_contact_phone': '612-208-6492',
                'emergency_contact_relationship': 'Sister',
                'social_media': 'hashed_social_1'
            },
            {
                'email': 'michael@allaboutpies.shop', 
                'password': 'password123',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'department': 'Kitchen',
                'position': 'Head Chef',
                'type': 'FULL_TIME',
                'phone': '612-555-1234',
                'salary': 65000.00
            },
            {
                'email': 'david@allaboutpies.shop',
                'password': 'password123', 
                'first_name': 'David',
                'last_name': 'Smith',
                'department': 'Service',
                'position': 'Server',
                'type': 'PART_TIME',
                'phone': '612-555-5678',
                'salary': 35000.00
            }
        ]

        for employee_data in sample_employees:
            if not cls.get_by_email(employee_data['email']):
                cls.create(**employee_data)