from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(allow_none=True)
    status = fields.Str(required=True, validate=validate.OneOf(
        ['Not Started', 'In-Progress', 'Completed', 'Approved']
    ))
    overall_risk = fields.Int(validate=validate.Range(min=0, max=5), default=0)
    max_vulnerability = fields.Int(validate=validate.Range(min=0, max=5), default=0)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
