from flask import Blueprint, request, jsonify
from management.models import PatientData
from common.services import validate_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.services import get_role
from common.constants import UserRole
from management.schema import PatientDataSchema, UpdateTestSchema
from common.exceptions import AuthError
from http import HTTPStatus
from management.services import (
    save_patient_data,
    get_patient_data,
    update_diabetes_test,
)
from db import db


management_bp = Blueprint("management_bp", __name__)


@management_bp.route("/", methods=["GET"])
@jwt_required()
def get_patient_data_response():
    user_id = get_jwt_identity()
    user_role = get_role(user_id)

    page = request.args.get("page", default=1, type=int)

    match user_role:
        case UserRole.PATIENT:
            paginated_data = PatientData.query.filter_by(patient_id=user_id).paginate(
                page=page, per_page=10
            )
        case UserRole.DOCTOR:
            paginated_data = PatientData.query.filter_by(doctor_id=user_id).paginate(
                page=page, per_page=10
            )
        case _:
            raise AuthError("Invalid user role", HTTPStatus.UNAUTHORIZED)

    schema = PatientDataSchema(many=True)

    return jsonify(message="Success", patient_data=schema.dump(paginated_data.items))


@management_bp.route("/", methods=["POST"])
@jwt_required()
def create_patient_data():
    user_id = get_jwt_identity()
    role = get_role(user_id)

    if role == UserRole.PATIENT:
        raise AuthError("You must be a doctor", HTTPStatus.UNAUTHORIZED)

    if role != UserRole.DOCTOR:
        raise AuthError("Invalid role", HTTPStatus.FORBIDDEN)

    data = request.get_json()
    schema = PatientDataSchema()
    patient_data: PatientData = validate_schema(data, schema)

    save_patient_data(patient_data)

    return jsonify(
        message="Successfully saved patient data",
        patient_data=schema.dump(patient_data),
    )


@management_bp.route("/", methods=["PUT"])
@jwt_required()
def update_patient_data():
    data = request.get_json()
    schema = UpdateTestSchema()
    patient_data_schema = PatientDataSchema()

    user_id = get_jwt_identity()
    role = get_role(user_id)

    if role != UserRole.DOCTOR:
        raise AuthError(
            "You are not allowed to complete a test", HTTPStatus.UNAUTHORIZED
        )

    validated_data = validate_schema(data, schema)

    patient_data = get_patient_data(validated_data["id"])  # type: ignore

    patient_data = update_diabetes_test(patient_data, validated_data["diabetes_test"])  # type: ignore

    return jsonify(
        message="Diabetes test updated successfully",
        patient_data=patient_data_schema.dump(patient_data),
    )
