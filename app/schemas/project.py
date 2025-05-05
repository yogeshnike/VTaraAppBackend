from marshmallow import Schema, fields, validate

class ProjectCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    created_by = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False, allow_none=True)
    status = fields.Str(required=True, validate=validate.OneOf(['Not-Started', 'In Progress', 'Completed']))
    overall_risk = fields.Float(required=True)
    max_vulnerability = fields.Float(required=True)

class ProjectUpdateSchema(ProjectCreateSchema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    created_by = fields.Str(required=False)
    start_date = fields.Date(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(['Not-Started', 'In Progress', 'Completed']))
    overall_risk = fields.Float(required=False)
    max_vulnerability = fields.Float(required=False)

class ProjectResponseSchema(ProjectCreateSchema):
    id = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    status = fields.String(validate=validate.OneOf(['Not-Started', 'In-Progress', 'Completed']))