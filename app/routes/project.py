from flask import Blueprint, request, jsonify
from app.models.project import Project
from app.extensions import db
from app.schemas.project import ProjectCreateSchema, ProjectUpdateSchema, ProjectResponseSchema
from marshmallow import ValidationError
from datetime import datetime
from app.models.configuration import Configuration 

bp = Blueprint('projects', __name__)
project_schema = ProjectResponseSchema()
projects_schema = ProjectResponseSchema(many=True)
project_create_schema = ProjectCreateSchema()
project_update_schema = ProjectUpdateSchema()

@bp.route('/projects', methods=['POST'])
def create_project():
    try:
        data = project_create_schema.load(request.json)
        # Validate that the configuration exists
        config = Configuration.query.get(data['config_id'])
        if not config:
            return jsonify({"error": "Configuration not found"}), 404
        project = Project(**data)
        db.session.add(project)
        db.session.commit()
        print(jsonify(project_schema.dump(project)))
        return jsonify(project_schema.dump(project)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify(projects_schema.dump(projects))

@bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project_schema.dump(project))

@bp.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        data = project_update_schema.load(request.json, partial=True)

        # Remove config_id from update data if it exists
        data.pop('config_id', None)
        
        for key, value in data.items():
            setattr(project, key, value)
        
        db.session.commit()
        return jsonify(project_schema.dump(project))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return '', 204

@bp.route('/projects/<project_id>/status', methods=['PATCH'])
def update_project_status(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        data = request.json
        
        # Validate status value
        valid_statuses = ['Not-Started', 'In-Progress', 'Completed']
        if 'status' not in data or data['status'] not in valid_statuses:
            return jsonify({
                "error": "Invalid status. Must be one of: Not-Started, In-Progress, Completed"
            }), 400
        
        # Update project status
        project.status = data['status']
        project.updated_at = datetime.utcnow()  # Update the timestamp
        
        db.session.commit()
        return jsonify(project_schema.dump(project))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Add a new endpoint to get available configurations for project creation
