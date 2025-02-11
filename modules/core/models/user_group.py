"""User-Group association table for managing user group memberships"""

from system.db.database import db
from system.db.decorators import ModelRegistry

# User-Group association table
user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.UniqueConstraint('user_id', 'group_id')
)

# Register the association table
ModelRegistry.register_table(user_group, "core") 