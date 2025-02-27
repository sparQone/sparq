from datetime import datetime
from system.db.database import db
from system.db.decorators import ModelRegistry

@ModelRegistry.register
class CompanySetting(db.Model):
    """Company-wide settings including email configuration"""
    __tablename__ = "company_setting"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, key, default=None):
        """Get a setting value by key"""
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default

    @classmethod
    def set(cls, key, value, description=None):
        """Set a setting value"""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = cls(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting

    # Email configuration methods
    @classmethod
    def get_email_settings(cls):
        """Get all email-related settings"""
        return {
            'sendgrid_api_key': cls.get('sendgrid_api_key', ''),
            'sendgrid_from_email': cls.get('sendgrid_from_email', ''),
            'sendgrid_from_name': cls.get('sendgrid_from_name', '')
        }

    @classmethod
    def update_email_settings(cls, api_key, from_email, from_name):
        """Update all email-related settings"""
        cls.set('sendgrid_api_key', api_key, 'SendGrid API Key')
        cls.set('sendgrid_from_email', from_email, 'SendGrid From Email')
        cls.set('sendgrid_from_name', from_name, 'SendGrid From Name') 