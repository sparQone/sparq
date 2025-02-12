from system.db.database import db


class CompanySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    default_language = db.Column(db.String(5), default='en')
    # other company settings... 