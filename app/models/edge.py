from datetime import datetime
from app.extensions import db
import uuid


class Edge(db.Model):
    __tablename__ = 'edges'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    source_node_id = db.Column(db.String(36), db.ForeignKey('nodes.id'), nullable=False)
    target_node_id = db.Column(db.String(36), db.ForeignKey('nodes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref=db.backref('edges', lazy=True))
    source_node = db.relationship('Node', foreign_keys=[source_node_id])
    target_node = db.relationship('Node', foreign_keys=[target_node_id])

    def to_dict(self):
        return {
            'id': self.id,
            'source_node_id': self.source_node_id,
            'target_node_id': self.target_node_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }