from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class Canvas(db.Model):
    __tablename__ = 'canvas'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String, db.ForeignKey('projects.id'), unique=True, nullable=False)
    data = db.Column(JSONB, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Canvas project_id={self.project_id} timestamp={self.timestamp}>"