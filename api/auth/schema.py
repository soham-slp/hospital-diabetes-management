from db import ma
from auth.models import User
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        exclude = ("password_hash", "id")

    name = ma.auto_field()
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    role = fields.Integer(required=False)
