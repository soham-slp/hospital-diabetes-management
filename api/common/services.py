from marshmallow import ValidationError, Schema
from common.exceptions import ValidationException

def validate_schema(data, schema: Schema):
    try:
        return schema.load(data)
    except ValidationError as e:
        raise ValidationException(e)