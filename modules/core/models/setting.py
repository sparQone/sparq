from datetime import datetime

from modules.core.models.user import User
from system.db.database import db


class UserSetting(db.Model):
    __tablename__ = "user_setting"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Create a composite unique constraint on user_id and key
    __table_args__ = (db.UniqueConstraint("user_id", "key", name="_user_setting_uc"),)

    # Relationship to User model
    user = db.relationship("User", backref=db.backref("settings", lazy=True))

    @staticmethod
    def get(user_id, key, default=None):
        setting = UserSetting.query.filter_by(user_id=user_id, key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set(user_id, key, value):
        try:
            # Try to update existing setting
            rows_updated = UserSetting.query.filter_by(user_id=user_id, key=key).update(
                {"value": value, "updated_at": datetime.utcnow()}, synchronize_session=False
            )

            # If no rows were updated, create new setting
            if rows_updated == 0:
                setting = UserSetting(user_id=user_id, key=key, value=value)
                db.session.add(setting)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error setting user setting: {e}")
            return False
