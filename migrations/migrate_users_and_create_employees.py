from flask import current_app
from system.db.database import db
from modules.core.models.user import User
from modules.people.models.employee import Employee
from modules.nickname.models import EmployeeNickname
from sqlalchemy import inspect, text

def migrate_database():
    with current_app.app_context():
        inspector = inspect(db.engine)
        
        # Create user table if it doesn't exist
        if not inspector.has_table('user'):
            User.__table__.create(db.engine)
            print("Created user table")
        
        # Create employee table if it doesn't exist
        if not inspector.has_table('employee'):
            Employee.__table__.create(db.engine)
            print("Created employee table")
            
        # Create employee_nickname table if it doesn't exist
        if not inspector.has_table('employee_nickname'):
            EmployeeNickname.__table__.create(db.engine)
            print("Created employee_nickname table")
        
        # If users table exists and has data, migrate it
        if inspector.has_table('users'):
            # Get all users from the users table
            result = db.session.execute(text('SELECT * FROM users'))
            users_data = result.fetchall()
            
            # Migrate each user
            for user in users_data:
                # Check if user already exists in user table
                if not User.query.filter_by(email=user.email).first():
                    new_user = User(
                        email=user.email,
                        password_hash=user.password_hash,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        is_active=user.is_active,
                        is_admin=user.is_admin,
                        created_at=user.created_at
                    )
                    db.session.add(new_user)
            
            db.session.commit()
            print("Migrated users data")
            
            # Drop the old users table
            db.session.execute(text('DROP TABLE IF EXISTS users'))
            db.session.commit()
            print("Dropped old users table") 