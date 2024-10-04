from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies
from auth.services import create_user
from common.services import validate_schema
from auth.schema import UserSchema

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    schema = UserSchema()

    validated_data = validate_schema(data, schema)
    
    user = create_user(validated_data['password'], name = validated_data['name'], email = validated_data['email'])
    
    return jsonify(
        message="Signup successful",
        created_user=schema.dump(user),
    )