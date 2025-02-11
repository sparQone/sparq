# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Task model that provides core task management functionality including
#     CRUD operations and sample data generation for the task management
#     module.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from system.db.database import db
from system.db.decorators import ModelRegistry

@ModelRegistry.register
class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_sample_data(cls):
        """Initialize sample tasks if table is empty"""
        if not cls.query.first():  # Only create if table is empty
            cls.create("Review project requirements")
            cls.create("Schedule team meeting")
            cls.create("Update documentation")
            print("Sample tasks created")

    @staticmethod
    def create(name):
        task = Task(name=name)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def delete(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()

    @staticmethod
    def update(task_id, name):
        task = Task.query.get(task_id)
        if task:
            task.name = name
            db.session.commit()
            return task
        return None
