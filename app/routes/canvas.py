from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.node import Node
from app.models.group import Group
from app.models.edge import Edge
from app.models.canvas import Canvas
from app.schemas.node import NodeSchema
from app.schemas.group import GroupSchema
from app.schemas.edge import EdgeSchema
from app.schemas.canvas import CanvasSchema
from marshmallow import ValidationError
from datetime import datetime

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

@bp.route('<project_id>/nodes/<node_id>/group', methods=['PUT'])
def update_node_group(project_id, node_id):
    try:
        data = request.get_json()
        node = Node.query.filter_by(project_id=project_id, id=node_id).first()
        
        if not node:
            return jsonify({'error': 'Node not found'}), 404

        # Validate group if group_id is provided
        group_id = data.get('group_id')
        if group_id:
            group = Group.query.filter_by(project_id=project_id, id=group_id).first()
            if not group:
                return jsonify({'error': 'Group not found'}), 404
            
        # Update node's group
        node.group_id = group_id
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
        print(data)
        data['project_id'] = project_id
        group_data = group_schema.load(data)
        group = Group(**group_data)
        db.session.add(group)
        db.session.commit()
        return jsonify(group_schema.dump(group)), 201
    except ValidationError as err:
        print(err.messages)
        return jsonify(err.messages), 400

@bp.route('<project_id>/groups/<group_id>', methods=['PUT'])
def update_group(project_id, group_id):
    try:
        data = request.get_json()
        group = Group.query.filter_by(project_id=project_id, id=group_id).first()
        
        if not group:
            return jsonify({'error': 'Group not found'}), 404
            
        # Update group fields
        group.group_name = data['group_name']
        if 'parent_group_id' in data:
            # Check for circular reference if parent_group_id is being updated
            if data['parent_group_id']:
                # Check if the new parent exists and belongs to the same project
                parent_group = Group.query.filter_by(
                    project_id=project_id, 
                    id=data['parent_group_id']
                ).first()
                
                if not parent_group:
                    return jsonify({'error': 'Parent group not found'}), 404
                
                # Check for circular reference
                current_parent = parent_group
                while current_parent:
                    if current_parent.id == group_id:
                        return jsonify({'error': 'Circular group reference detected'}), 400
                    current_parent = current_parent.parent_group_id and Group.query.get(current_parent.parent_group_id)
            
            group.parent_group_id = data['parent_group_id']
        
        db.session.commit()
        return jsonify(group_schema.dump(group)), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('<project_id>/groups/<group_id>', methods=['DELETE'])
def delete_group(project_id, group_id):
    try:
        group = Group.query.filter_by(project_id=project_id, id=group_id).first()
        
        if not group:
            return jsonify({'error': 'Group not found'}), 404
            
        # Update child nodes to remove group reference
        Node.query.filter_by(group_id=group_id).update({'group_id': None})
        
        # Update child groups to remove parent reference
        Group.query.filter_by(parent_group_id=group_id).update({'parent_group_id': None})
        
        # Delete the group
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({'message': 'Group deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('<project_id>/edges', methods=['POST'])
def create_edge(project_id):
    try:
        data = request.get_json()
        data['project_id'] = project_id
        
        
       
        print(data)
            
        # Validate source and target nodes exist and belong to the project
        source_node = Node.query.filter_by(
            project_id=project_id, 
            id=data['source_node_id']
        ).first()
        target_node = Node.query.filter_by(
            project_id=project_id, 
            id=data['target_node_id']
        ).first()
        
        
        if not source_node or not target_node:
            return jsonify({'error': 'Source or target node not found'}), 404
            
        # Set empty string as default for edge_label if not provided
        if 'edge_label' not in data:
            data['edge_label'] = ''
            
        edge_data = edge_schema.load(data)
        edge = Edge(**edge_data)
        db.session.add(edge)
        db.session.commit()
        
        return jsonify(edge_schema.dump(edge)), 201
        
    except ValidationError as err:
        print(err.messages)
        return jsonify(err.messages), 400
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('<project_id>/edges/<edge_id>', methods=['PUT'])
def update_edge(project_id, edge_id):
    try:
        data = request.get_json()
        edge = Edge.query.filter_by(project_id=project_id, id=edge_id).first()
        
        if not edge:
            return jsonify({'error': 'Edge not found'}), 404
            
        edge.edge_label = data['edge_label']
        db.session.commit()
        
        return jsonify(edge_schema.dump(edge)), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('<project_id>/edges/<edge_id>', methods=['DELETE'])
def delete_edge(project_id, edge_id):
    try:
        edge = Edge.query.filter_by(project_id=project_id, id=edge_id).first()
        
        if not edge:
            return jsonify({'error': 'Edge not found'}), 404
            
        # Delete the edge
        db.session.delete(edge)
        db.session.commit()
        
        return jsonify({'message': 'Edge deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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

@bp.route('<project_id>/canvass', methods=['POST'])
def save_canvasbp(project_id):
    try:
        data = request.get_json()
        print(data)
        
        # Start transaction
        db.session.begin_nested()
        
        # Delete existing canvas data
        Edge.query.filter_by(project_id=project_id).delete()
        Node.query.filter_by(project_id=project_id).delete()
        Group.query.filter_by(project_id=project_id).delete()
        
        
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
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('<project_id>/canvas', methods=['POST'])
def save_canvas(project_id):
    try:
        data = request.get_json()
        print(data)

        # --- 1. Update/Insert Groups ---
        incoming_group_ids = set()
        for group_data in data.get('groups', []):
            group_data['project_id'] = project_id
            group = Group.query.filter_by(project_id=project_id, id=group_data['id']).first()
            if group:
                # Update existing
                group.group_name = group_data['group_name']
                group.x_pos = group_data.get('x_pos', group.x_pos)
                group.y_pos = group_data.get('y_pos', group.y_pos)
                group.parent_group_id = group_data.get('parent_group_id')
                group.width = group_data.get('width', group.width)
                group.height = group_data.get('height', group.height)
                #group.style = group_data.get('style', group.style)
            else:
                # Insert new
                group = Group(**group_schema.load(group_data))
                db.session.add(group)
            incoming_group_ids.add(group_data['id'])

        # Delete groups not in incoming data
        Group.query.filter(
            Group.project_id == project_id,
            ~Group.id.in_(incoming_group_ids)
        ).delete(synchronize_session=False)

        db.session.flush()  # To get group IDs for nodes

        # --- 2. Update/Insert Nodes ---
        incoming_node_ids = set()
        for node_data in data.get('nodes', []):
            node_data['project_id'] = project_id
            node = Node.query.filter_by(project_id=project_id, id=node_data['id']).first()
            if node:
                # Update existing
                node.node_name = node_data['node_name']
                node.node_description = node_data['node_description']
                node.x_pos = node_data['x_pos']
                node.y_pos = node_data['y_pos']
                node.stride_properties = node_data['stride_properties']
                node.group_id = node_data.get('group_id')
            else:
                # Insert new
                node = Node(**node_schema.load(node_data))
                db.session.add(node)
            incoming_node_ids.add(node_data['id'])

        # Delete nodes not in incoming data
        Node.query.filter(
            Node.project_id == project_id,
            ~Node.id.in_(incoming_node_ids)
        ).delete(synchronize_session=False)

        db.session.flush()  # To get node IDs for edges

         # --- 3. Update/Insert Edges ---
        incoming_edge_ids = set()
        for edge_data in data.get('edges', []):
            edge_data['project_id'] = project_id
            edge = Edge.query.filter_by(project_id=project_id, id=edge_data['id']).first()
            if edge:
                # Update existing
                edge.source_node_id = edge_data['source_node_id']
                edge.target_node_id = edge_data['target_node_id']
                edge.edge_label = edge_data.get('edge_label', '')
                edge.style = edge_data.get('style', edge.style)
            else:
                # Insert new
                edge = Edge(**edge_schema.load(edge_data))
                db.session.add(edge)
            incoming_edge_ids.add(edge_data['id'])

        # Delete edges not in incoming data
        Edge.query.filter(
            Edge.project_id == project_id,
            ~Edge.id.in_(incoming_edge_ids)
        ).delete(synchronize_session=False)

        # --- 4. Save Canvas JSON ---
        canvas = Canvas.query.filter_by(project_id=project_id).first()
        if not canvas:
            canvas = Canvas(
                project_id=project_id,
                data=data,
                timestamp=datetime.utcnow()
            )
            db.session.add(canvas)
        else:
            canvas.data = data
            canvas.timestamp = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Canvas saved successfully'}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 400