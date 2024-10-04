from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_refresh_cookies,
    unset_refresh_cookies,
    create_access_token,
    get_csrf_token,
)
from auth.services import create_user, get_user, validate_password
from common.services import validate_schema
from auth.schema import UserSchema

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    schema = UserSchema()

    validated_data = validate_schema(data, schema)

    user = create_user(
        validated_data["password"],
        name=validated_data["name"],
        email=validated_data["email"],
    )

    return jsonify(
        message="Signup successful",
        created_user=schema.dump(user),
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    schema = UserSchema()

    validated_data = validate_schema(data, schema)

    user = get_user(name=validated_data["name"], email=validated_data["email"])

    validate_password(validated_data["password"], user)

    identity = user.id

    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    csrf_token = get_csrf_token(refresh_token)

    response = jsonify(
        message="Login successful",
        logged_in_user=schema.dump(user),
        access_token=access_token,
        csrf_token=csrf_token,
    )

    set_refresh_cookies(response, refresh_token)

    return response


@auth_bp.route("/logout", methods=["GET"])
@jwt_required(refresh=True, locations=["cookies"])
def logout():
    response = jsonify(message="Logout succesful!")

    unset_refresh_cookies(response)

    return response


@auth_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True, locations=["cookies"])
def refresh():
    identity = get_jwt_identity()

    user = get_user(user_id=identity)

    access_token = create_access_token(user.id)

    return jsonify(message="Refresh succesful!", access_token=access_token)
