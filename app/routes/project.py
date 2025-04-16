from flask import Blueprint, request, jsonify
from app.models.project import Project
from app.extensions import db
from app.schemas.project import ProjectCreateSchema, ProjectUpdateSchema, ProjectResponseSchema
from marshmallow import ValidationError
from datetime import datetime

bp = Blueprint('projects', __name__)
project_schema = ProjectResponseSchema()
projects_schema = ProjectResponseSchema(many=True)
project_create_schema = ProjectCreateSchema()
project_update_schema = ProjectUpdateSchema()

@bp.route('/projects', methods=['POST'])
def create_project():
    try:
        data = project_create_schema.load(request.json)
        project = Project(**data)
        db.session.add(project)
        db.session.commit()
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