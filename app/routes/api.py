from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project
from app.schemas.project import ProjectSchema
from marshmallow import ValidationError

bp = Blueprint('api', __name__, url_prefix='/api/v1')
project_schema = ProjectSchema()

@bp.route('/projects', methods=['POST'])
def create_project():
    try:
        # Validate and deserialize input
        project_data = project_schema.load(request.json)
        
        # Create new project
        project = Project(
            name=project_data['name'],
            description=project_data['description'],
            start_date=project_data['start_date'],
            end_date=project_data.get('end_date'),
            status=project_data['status'],
            overall_risk=project_data.get('overall_risk', 0),
            max_vulnerability=project_data.get('max_vulnerability', 0)
        )
        
        # Save to database
        db.session.add(project)
        db.session.commit()
        
        # Return created project
        return jsonify(project_schema.dump(project)), 201
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
