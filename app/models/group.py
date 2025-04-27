from datetime import datetime
from app.extensions import db
import uuid



class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    group_name = db.Column(db.String(255), nullable=False)
    parent_group_id = db.Column(db.String(36), db.ForeignKey('groups.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref=db.backref('groups', lazy=True))
    parent_group = db.relationship('Group', backref=db.backref('child_groups', lazy=True),
                                 remote_side=[id])

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'parent_group_id': self.parent_group_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }