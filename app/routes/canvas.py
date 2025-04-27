from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.node import Node
from app.models.group import Group
from app.models.edge import Edge
from app.schemas.node import NodeSchema
from app.schemas.group import GroupSchema
from app.schemas.edge import EdgeSchema
from marshmallow import ValidationError

bp = Blueprint('canvas', __name__)
node_schema = NodeSchema()
group_schema = GroupSchema()
edge_schema = EdgeSchema()

@bp.route('<project_id>/nodes', methods=['POST'])
def create_node(project_id):
    try:
        data = request.get_json()
        print(data)
        data['project_id'] = project_id
        node_data = node_schema.load(data)
        node = Node(**node_data)
        db.session.add(node)
        db.session.commit()
        return jsonify(node_schema.dump(node)), 201
    except ValidationError as err:
        print(err.messages)
        return jsonify(err.messages), 400

# Add this route after create_node route
@bp.route('<project_id>/nodes/<node_id>', methods=['PUT'])
def update_node(project_id, node_id):
    try:
        data = request.get_json()
        node = Node.query.filter_by(project_id=project_id, id=node_id).first()
        
        if not node:
            return jsonify({'error': 'Node not found'}), 404
            
        # Update node fields
        node.node_name = data['node_name']
        node.node_description = data['node_description']
        node.stride_properties = data['stride_properties']
        
        db.session.commit()
        
        return jsonify(node_schema.dump(node)), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Add this route after update_node route
@bp.route('<project_id>/nodes/<node_id>', methods=['DELETE'])
def delete_node(project_id, node_id):
    try:
        node = Node.query.filter_by(project_id=project_id, id=node_id).first()
        
        if not node:
            return jsonify({'error': 'Node not found'}), 404
            
        # Delete any edges connected to this node
        Edge.query.filter(
            (Edge.source_node_id == node_id) | 
            (Edge.target_node_id == node_id)
        ).delete()
        
        # Delete the node
        db.session.delete(node)
        db.session.commit()
        
        return jsonify({'message': 'Node deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('<project_id>/groups', methods=['POST'])
def create_group(project_id):
    try:
        data = request.get_json()
        data['project_id'] = project_id
        group_data = group_schema.load(data)
        group = Group(**group_data)
        db.session.add(group)
        db.session.commit()
        return jsonify(group_schema.dump(group)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@bp.route('<project_id>/edges', methods=['POST'])
def create_edge(project_id):
    try:
        data = request.get_json()
        data['project_id'] = project_id
        edge_data = edge_schema.load(data)
        edge = Edge(**edge_data)
        db.session.add(edge)
        db.session.commit()
        return jsonify(edge_schema.dump(edge)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@bp.route('<project_id>/canvas', methods=['GET'])
def get_canvas(project_id):
    nodes = Node.query.filter_by(project_id=project_id).all()
    groups = Group.query.filter_by(project_id=project_id).all()
    edges = Edge.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'nodes': [node_schema.dump(node) for node in nodes],
        'groups': [group_schema.dump(group) for group in groups],
        'edges': [edge_schema.dump(edge) for edge in edges]
    })

@bp.route('<project_id>/canvas', methods=['POST'])
def save_canvas(project_id):
    try:
        data = request.get_json()
        
        # Start transaction
        db.session.begin_nested()
        
        # Delete existing canvas data
        Node.query.filter_by(project_id=project_id).delete()
        Group.query.filter_by(project_id=project_id).delete()
        Edge.query.filter_by(project_id=project_id).delete()
        
        # Create groups first (for hierarchy)
        group_map = {}
        for group_data in data.get('groups', []):
            group_data['project_id'] = project_id
            group = Group(**group_schema.load(group_data))
            db.session.add(group)
            db.session.flush()
            group_map[group_data['id']] = group.id
        
        # Update parent group references
        for group in Group.query.filter_by(project_id=project_id).all():
            if group.parent_group_id in group_map:
                group.parent_group_id = group_map[group.parent_group_id]
        
        # Create nodes
        node_map = {}
        for node_data in data.get('nodes', []):
            node_data['project_id'] = project_id
            if node_data.get('group_id') in group_map:
                node_data['group_id'] = group_map[node_data['group_id']]
            node = Node(**node_schema.load(node_data))
            db.session.add(node)
            db.session.flush()
            node_map[node_data['id']] = node.id
        
        # Create edges
        for edge_data in data.get('edges', []):
            edge_data['project_id'] = project_id
            edge_data['source_node_id'] = node_map[edge_data['source_node_id']]
            edge_data['target_node_id'] = node_map[edge_data['target_node_id']]
            edge = Edge(**edge_schema.load(edge_data))
            db.session.add(edge)
        
        db.session.commit()
        return jsonify({'message': 'Canvas saved successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400