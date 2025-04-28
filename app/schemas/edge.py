from marshmallow import Schema, fields,validate

class EdgeSchema(Schema):
    id = fields.Str(dump_only=True)
    project_id = fields.Str(required=True)
    source_node_id = fields.Str(required=True)
    target_node_id = fields.Str(required=True)
    edge_label = fields.Str(allow_none=True, validate=validate.Length(max=255))
    style = fields.Dict()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)