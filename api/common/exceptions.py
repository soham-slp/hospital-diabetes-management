from common.constants import ExceptionType
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus

class CustomBaseException(Exception):
    def __init__(self, message: str, error_type: ExceptionType, status: HTTPStatus):
        self.message = message
        self.error_type = error_type
        self.status = status

class DBException(CustomBaseException):
    def __init__(self, error: SQLAlchemyError):
        message = f"Error in database: {error}"
        
        super().__init__(message, ExceptionType.DB, HTTPStatus.INTERNAL_SERVER_ERROR)
