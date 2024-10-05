from enum import IntEnum


class ExceptionType(IntEnum):
    UNKNOWN = -1
    DB = 1
    VALIDATION = 2
    AUTH = 3
    LOGICAL = 4
    NOT_FOUND = 5


class UserRole(IntEnum):
    DOCTOR = 0
    PATIENT = 1
