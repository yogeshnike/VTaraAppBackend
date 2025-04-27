from marshmallow import Schema, fields

class EdgeSchema(Schema):
    id = fields.Str(dump_only=True)
    project_id = fields.Str(required=True)
    source_node_id = fields.Str(required=True)
    target_node_id = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)