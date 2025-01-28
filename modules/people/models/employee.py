from system.db.database import db
from enum import Enum
from modules.core.models.user import User

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

    @classmethod
    def create(cls, user, **kwargs):
        """Create new employee profile"""
        employee = cls(user=user, **kwargs)
        db.session.add(employee)
        db.session.commit()
        return employee 