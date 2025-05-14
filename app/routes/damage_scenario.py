from flask import Blueprint, request, jsonify
from app.models.damage_scenario import DamageScenario
from app.models.config_damage_scenario import ConfigurationDamageScenario
from app.models.project_damage_scenario import ProjectDamageScenario
from app.extensions import db
from app.schemas.damage_scenario import (
    DamageScenarioCreateSchema,
    DamageScenarioResponseSchema
)
from marshmallow import ValidationError
import json

bp = Blueprint('damage_scenarios', __name__)

damage_scenario_schema = DamageScenarioResponseSchema()
damage_scenarios_schema = DamageScenarioResponseSchema(many=True)
damage_scenario_create_schema = DamageScenarioCreateSchema()

@bp.route('/damage-scenarios', methods=['POST'])
def create_damage_scenario():
    try:
         # Extract config_id before validation
        request_data = request.json.copy()  # Make a copy to avoid modifying the original
        config_id = request_data.pop('config_id', None)  # Remove and store config_id
        
        print("Data for validation:", request_data)  # Debug log
        data = damage_scenario_create_schema.load(request_data)  # Validate remaining data
        
        damage_scenario = DamageScenario(**data)
        db.session.add(damage_scenario)
        db.session.commit()
        
        # If config_id was present, create the configuration link
        if config_id:
            config_link = ConfigurationDamageScenario(
                config_id=config_id,
                damage_scenario_id=damage_scenario.id
            )
            db.session.add(config_link)
            db.session.commit()

         # Parse the JSON strings before returning
        result = damage_scenario_schema.dump(damage_scenario)
        # Ensure road_users and business are parsed from JSON strings to objects
        result['road_users'] = json.loads(damage_scenario.road_users)
        result['business'] = json.loads(damage_scenario.business)
        
        return jsonify(result), 201
    except ValidationError as err:
        print("Validation error:", err.messages)  # Debug log
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        print("Error:", str(e))  # Debug log
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/damage-scenarios', methods=['GET'])
def get_damage_scenarios():
    try:
        config_id = request.args.get('config_id')
        project_id = request.args.get('project_id')
        
        if config_id:
            # Get damage scenarios linked to the configuration
            links = ConfigurationDamageScenario.query.filter_by(config_id=config_id).all()
            scenario_ids = [link.damage_scenario_id for link in links]
            scenarios = DamageScenario.query.filter(DamageScenario.id.in_(scenario_ids)).all()
        elif project_id:
            # Get damage scenarios linked to the project
            links = ProjectDamageScenario.query.filter_by(project_id=project_id).all()
            scenario_ids = [link.damage_scenario_id for link in links]
            scenarios = DamageScenario.query.filter(DamageScenario.id.in_(scenario_ids)).all()
        else:
            # Get all damage scenarios
            scenarios = DamageScenario.query.all()
        
         # Parse JSON strings before returning
        result = []
        for scenario in scenarios:
            scenario_data = damage_scenario_schema.dump(scenario)
            # Parse road_users and business only if they are strings
            if isinstance(scenario.road_users, str):
                scenario_data['road_users'] = json.loads(scenario.road_users)
            if isinstance(scenario.business, str):
                scenario_data['business'] = json.loads(scenario.business)
            result.append(scenario_data)
        
        return jsonify(result)
    except Exception as e:
        print("Error in get_damage_scenarios:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

@bp.route('/damage-scenarios/<id>', methods=['GET'])
def get_damage_scenario(id):
    try:
        damage_scenario = DamageScenario.query.get_or_404(id)
        return jsonify(damage_scenario_schema.dump(damage_scenario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/damage-scenarios/<id>', methods=['PUT'])
def update_damage_scenario(id):
    try:
        damage_scenario = DamageScenario.query.get_or_404(id)
        data = damage_scenario_create_schema.load(request.json, partial=True)
        
        for key, value in data.items():
            setattr(damage_scenario, key, value)
        
        db.session.commit()
        return jsonify(damage_scenario_schema.dump(damage_scenario))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/damage-scenarios/<id>', methods=['DELETE'])
def delete_damage_scenario(id):
    try:
        damage_scenario = DamageScenario.query.get_or_404(id)
        
        # Delete all related links
        ConfigurationDamageScenario.query.filter_by(damage_scenario_id=id).delete()
        ProjectDamageScenario.query.filter_by(damage_scenario_id=id).delete()
        
        db.session.delete(damage_scenario)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/projects/<project_id>/damage-scenarios/bulk', methods=['POST'])
def add_scenarios_to_project(project_id):
    try:
        scenario_ids = request.json.get('scenario_ids', [])
        
        for scenario_id in scenario_ids:
            # Check if link already exists
            existing = ProjectDamageScenario.query.filter_by(
                project_id=project_id,
                damage_scenario_id=scenario_id
            ).first()
            
            if not existing:
                link = ProjectDamageScenario(
                    project_id=project_id,
                    damage_scenario_id=scenario_id
                )
                db.session.add(link)
        
        db.session.commit()
        return jsonify({"message": "Damage scenarios added to project"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500