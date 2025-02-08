# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Nickname module models for employee nickname management.
#     Handles the creation and updating of employee nicknames.
#
# Copyright (c) 2025 remarQable LLC
from flask import current_app
from sqlalchemy import inspect

from modules.people.models.employee import Employee
from system.db.database import db
from system.db.decorators import ModelRegistry


@ModelRegistry.register
class EmployeeNickname(db.Model):
    """Extension table for employee nicknames"""

    __tablename__ = "employee_nickname"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relationship back to employee
    employee = db.relationship("Employee", backref=db.backref("nickname_data", uselist=False))

    @classmethod
    def create_or_update(cls, employee, nickname):
        """Create or update nickname for an employee"""
        # Ensure table exists
        inspector = inspect(db.engine)
        if not inspector.has_table("employee_nickname"):
            cls.__table__.create(db.engine)
            print("Created employee_nickname table")

        nickname_record = cls.query.filter_by(employee_id=employee.id).first()
        if nickname_record:
            nickname_record.nickname = nickname
        else:
            nickname_record = cls(employee_id=employee.id, nickname=nickname)
            db.session.add(nickname_record)
        db.session.commit()
        return nickname_record


class NicknameModel:
    def __init__(self):
        pass  # Remove table creation from init

    def save(self, data):
        """Save nickname data"""
        if "nickname" in data and hasattr(data, "employee"):
            EmployeeNickname.create_or_update(data.employee, data["nickname"])
            print(f"Saved nickname: {data['nickname']} for employee {data.employee.id}")
