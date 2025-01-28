from modules.people.models.employee import Employee
from system.db.database import db

class NicknameModel:
    def __init__(self):
        # Add nickname column to Employee model
        if not hasattr(Employee, 'nickname'):
            Employee.nickname = db.Column(db.String(50))

    def save(self, data):
        """Save nickname data"""
        if 'nickname' in data:
            print(f"Nickname module saving nickname: {data['nickname']}") 