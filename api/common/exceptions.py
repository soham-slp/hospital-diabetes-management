from common.constants import ExceptionType
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from marshmallow import ValidationError
import json


class CustomBaseException(Exception):
    def __init__(self, message: str, error_type: ExceptionType, status: HTTPStatus):
        self.message = message
        self.error_type = error_type
        self.status = status
        self.payload = None


class DBException(CustomBaseException):
    def __init__(self, error: SQLAlchemyError):
        message = f"Error in database: {error}"

        super().__init__(message, ExceptionType.DB, HTTPStatus.INTERNAL_SERVER_ERROR)


class ValidationException(CustomBaseException):
    def __init__(self, err: ValidationError):
        message = f"Error in validation: {json.dumps(err.messages)}"
        super().__init__(message, ExceptionType.VALIDATION, HTTPStatus.BAD_REQUEST)


class AuthError(CustomBaseException):
    def __init__(self, message: str, status: HTTPStatus):
        message = f"Error in auth: { message }"

        super().__init__(message, ExceptionType.AUTH, status)
