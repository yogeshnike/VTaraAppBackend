#Schema for validations
from marshmallow import Schema, fields, validate



class NodeSchema(Schema):
    id = fields.Str(dump_only=True)
    project_id = fields.Str(required=True)
    node_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    node_description = fields.Str()
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    stride_properties = fields.Dict()
    group_id = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
 