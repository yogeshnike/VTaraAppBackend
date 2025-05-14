from datetime import datetime
from app.extensions import db
import uuid

class ProjectDamageScenario(db.Model):
    __tablename__ = 'project_damage_scenarios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    damage_scenario_id = db.Column(db.String(36), db.ForeignKey('damage_scenarios.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add unique constraint to prevent duplicate links
    __table_args__ = (
        db.UniqueConstraint('project_id', 'damage_scenario_id', name='uix_project_damage'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'damage_scenario_id': self.damage_scenario_id,
            'created_at': self.created_at.isoformat()
        }