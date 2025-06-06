from marshmallow import Schema, fields, validate

class GroupSchema(Schema):
    id = fields.Str(dump_only=True)
    project_id = fields.Str(required=True)
    group_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    style = fields.Dict()
    parent_group_id = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)