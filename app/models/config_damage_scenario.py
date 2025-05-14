from datetime import datetime
from app.extensions import db
import uuid

class ConfigurationDamageScenario(db.Model):
    __tablename__ = 'configuration_damage_scenarios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    config_id = db.Column(db.String(36), db.ForeignKey('configurations.id'), nullable=False)
    damage_scenario_id = db.Column(db.String(36), db.ForeignKey('damage_scenarios.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add unique constraint to prevent duplicate links
    __table_args__ = (
        db.UniqueConstraint('config_id', 'damage_scenario_id', name='uix_config_damage'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'config_id': self.config_id,
            'damage_scenario_id': self.damage_scenario_id,
            'created_at': self.created_at.isoformat()
        }