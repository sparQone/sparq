from system.db.database import db

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

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