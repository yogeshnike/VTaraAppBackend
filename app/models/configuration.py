from app.extensions import db
from datetime import datetime

class Configuration(db.Model):
    __tablename__ = 'configurations'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(36), nullable=True)  # Optional: if you want to track who created it