from flask import Blueprint, jsonify
from http import HTTPStatus
from common.exceptions import ExceptionType, CustomBaseException

error_bp = Blueprint("error_bp", __name__)


@error_bp.app_errorhandler(CustomBaseException)
def base_exception(err: CustomBaseException):
    return jsonify(message=err.message, error_type=err.error_type), err.status


@error_bp.app_errorhandler(Exception)
def unknown_exception(err: Exception):
    return (
        jsonify(message=err.args[0], error_type=ExceptionType.UNKNOWN),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
