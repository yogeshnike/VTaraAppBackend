from marshmallow import Schema, fields

class CanvasSchema(Schema):
    id = fields.Int(dump_only=True)
    project_id = fields.Str(required=True)
    data = fields.Raw(required=True)  # Use Raw for arbitrary JSON
    timestamp = fields.DateTime()