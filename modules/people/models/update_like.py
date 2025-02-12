from system.db.database import db
from system.db.decorators import ModelRegistry


@ModelRegistry.register
class UpdateLike(db.Model):
    """Model for tracking likes on updates"""

    __tablename__ = "update_like"

    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey("update.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Create a unique constraint to prevent duplicate likes
    __table_args__ = (db.UniqueConstraint("update_id", "user_id", name="_update_like_uc"),)

    # Relationships
    user = db.relationship("User", backref=db.backref("update_likes", lazy="dynamic"))
