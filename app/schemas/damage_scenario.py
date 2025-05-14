from marshmallow import Schema, fields, validate

class ImpactValueSchema(Schema):
    value = fields.Str(required=True)
    justification = fields.Str(required=True)

class RoadUsersSchema(Schema):
    overall = fields.Str(required=True)
    values = fields.Dict(keys=fields.Str(), values=fields.Nested(ImpactValueSchema))

class BusinessSchema(Schema):
    overall = fields.Str(required=True)
    values = fields.Dict(keys=fields.Str(), values=fields.Nested(ImpactValueSchema))

class DamageScenarioCreateSchema(Schema):
    name = fields.Str(required=True)
    justification = fields.Str(required=True)
    security_property = fields.Str(
        required=True,
        validate=validate.OneOf(['N/A', 'Confidentiality(C)', 'Integrity(I)', 'Availability(A)'])
    )
    controlability = fields.Str(
        required=True,
        validate=validate.OneOf(['N/A', '1', '2', '3', '4'])
    )
    corporate_flag = fields.Str(
        required=True,
        validate=validate.OneOf([
            'Impact on road user safety',
            'Legal/Data Breach',
            'Certification/Emission Issue',
            'Material IP',
            'Financial Impact on Company'
        ])
    )
    road_users = fields.Nested(RoadUsersSchema, required=True)
    business = fields.Nested(BusinessSchema, required=True)

class DamageScenarioResponseSchema(DamageScenarioCreateSchema):
    id = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)