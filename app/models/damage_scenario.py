from datetime import datetime
from app.extensions import db
import uuid
import json

class DamageScenario(db.Model):
    __tablename__ = 'damage_scenarios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    security_property = db.Column(
        db.String(20), 
        nullable=False,
        default='N/A'
    )
    controlability = db.Column(
        db.String(10), 
        nullable=False,
        default='N/A'
    )
    corporate_flag = db.Column(
        db.String(50), 
        nullable=False
    )
    
    # Store JSON data in Text columns
    road_users = db.Column(db.Text, nullable=False)
    business = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        # Handle JSON fields
        road_users = kwargs.pop('road_users', {
            'overall': 'N/A',
            'values': {
                'safety': {'value': 'N/A', 'justification': ''},
                'privacy': {'value': 'N/A', 'justification': ''},
                'financial': {'value': 'N/A', 'justification': ''},
                'operational': {'value': 'N/A', 'justification': ''}
            }
        })
        business = kwargs.pop('business', {
            'overall': 'N/A',
            'values': {
                'ip': {'value': 'N/A', 'justification': ''},
                'financial': {'value': 'N/A', 'justification': ''},
                'brand': {'value': 'N/A', 'justification': ''}
            }
        })
        
        # Store JSON as string
        self.road_users = json.dumps(road_users)
        self.business = json.dumps(business)
        
        super().__init__(**kwargs)

    @property
    def road_users_data(self):
        """Get road_users as dictionary"""
        return json.loads(self.road_users)

    @road_users_data.setter
    def road_users_data(self, value):
        """Set road_users from dictionary"""
        self.road_users = json.dumps(value)

    @property
    def business_data(self):
        """Get business as dictionary"""
        return json.loads(self.business)

    @business_data.setter
    def business_data(self, value):
        """Set business from dictionary"""
        self.business = json.dumps(value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'justification': self.justification,
            'security_property': self.security_property,
            'controlability': self.controlability,
            'corporate_flag': self.corporate_flag,
            'road_users': self.road_users_data,
            'business': self.business_data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    # Add validation methods
    @staticmethod
    def validate_security_property(value):
        valid_values = ['N/A', 'Confidentiality(C)', 'Integrity(I)', 'Availability(A)']
        if value not in valid_values:
            raise ValueError(f'Invalid security property. Must be one of: {valid_values}')
        return value

    @staticmethod
    def validate_controlability(value):
        valid_values = ['N/A', '1', '2', '3', '4']
        if value not in valid_values:
            raise ValueError(f'Invalid controlability. Must be one of: {valid_values}')
        return value

    @staticmethod
    def validate_corporate_flag(value):
        valid_values = [
            'Impact on road user safety',
            'Legal/Data Breach',
            'Certification/Emission Issue',
            'Material IP',
            'Financial Impact on Company'
        ]
        if value not in valid_values:
            raise ValueError(f'Invalid corporate flag. Must be one of: {valid_values}')
        return value