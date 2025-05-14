from marshmallow import Schema, fields, validate

class ConfigurationBaseSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))

class ConfigurationCreateSchema(ConfigurationBaseSchema):
    pass

class ConfigurationUpdateSchema(ConfigurationBaseSchema):
    pass

class ConfigurationResponseSchema(ConfigurationBaseSchema):
    id = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_by = fields.String(dump_only=True)