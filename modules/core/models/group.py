from system.db.database import db
from system.db.decorators import ModelRegistry


@ModelRegistry.register
class Group(db.Model):
    """Group model for user access control"""

    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    is_system = db.Column(db.Boolean, default=False)

    @classmethod
    def get_or_create(cls, name, description=None, is_system=False):
        """Get existing group or create new one"""
        group = cls.query.filter_by(name=name).first()
        if not group:
            group = cls(name=name, description=description, is_system=is_system)
            db.session.add(group)
            db.session.commit()
        return group

    @classmethod
    def get_admin_group(cls):
        """Get ADMIN group"""
        return cls.query.filter_by(name="ADMIN").first()

    @classmethod
    def get_all_group(cls):
        """Get ALL group"""
        return cls.query.filter_by(name="ALL").first()

    def __repr__(self):
        return f"<Group {self.name}>"
