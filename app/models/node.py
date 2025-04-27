from datetime import datetime
from app.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import JSONB

from marshmallow import Schema, fields, validate
class Node(db.Model):
    __tablename__ = 'nodes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    node_name = db.Column(db.String(255), nullable=False)
    node_description = db.Column(db.Text, nullable=True)
    x_pos = db.Column(db.Float, nullable=False)
    y_pos = db.Column(db.Float, nullable=False)
    stride_properties = db.Column(JSONB, nullable=True)
    group_id = db.Column(db.String(36), db.ForeignKey('groups.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref=db.backref('nodes', lazy=True))
    group = db.relationship('Group', backref=db.backref('nodes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'node_name': self.node_name,
            'node_description': self.node_description,
            'x_pos': self.x_pos,
            'y_pos': self.y_pos,
            'stride_properties': self.stride_properties,
            'group_id': self.group_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }