from flask import Blueprint, request, jsonify
from app.models.configuration import Configuration
from app.extensions import db
from app.schemas.configuration import (
    ConfigurationCreateSchema,
    ConfigurationUpdateSchema,
    ConfigurationResponseSchema
)
from marshmallow import ValidationError
from datetime import datetime
import uuid

bp = Blueprint('configurations', __name__)

configuration_schema = ConfigurationResponseSchema()
configurations_schema = ConfigurationResponseSchema(many=True)
configuration_create_schema = ConfigurationCreateSchema()
configuration_update_schema = ConfigurationUpdateSchema()

@bp.route('/configurations', methods=['GET'])
def get_configurations():
    print("came here")
    configurations = Configuration.query.all()
    return jsonify(configurations_schema.dump(configurations))

@bp.route('/configurations/<configuration_id>', methods=['GET'])
def get_configuration(configuration_id):
    
    configuration = Configuration.query.get_or_404(configuration_id)
    return jsonify(configuration_schema.dump(configuration))

@bp.route('/configurations', methods=['POST'])
def create_configuration():
    try:
        data = configuration_create_schema.load(request.json)
        configuration = Configuration(
            id=str(uuid.uuid4()),
            name=data['name']
        )
        db.session.add(configuration)
        db.session.commit()
        return jsonify(configuration_schema.dump(configuration)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@bp.route('/configurations/<configuration_id>', methods=['PUT'])
def update_configuration(configuration_id):
    try:
        configuration = Configuration.query.get_or_404(configuration_id)
        data = configuration_update_schema.load(request.json)
        
        for key, value in data.items():
            setattr(configuration, key, value)
        
        configuration.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(configuration_schema.dump(configuration))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@bp.route('/configurations/<configuration_id>', methods=['DELETE'])
def delete_configuration(configuration_id):
    configuration = Configuration.query.get_or_404(configuration_id)
    db.session.delete(configuration)
    db.session.commit()
    return '', 204