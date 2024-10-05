from common.constants import UserRole
from auth.models import User
from common.exceptions import AuthError, DBException
from http import HTTPStatus
from db import db
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from flask import current_app
from typing import Optional


def get_user(
    user_id: Optional[int] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
) -> User:
    if user_id:
        user = User.query.get(user_id)
    elif name is not None and email is not None:
        user = User.query.filter_by(name=name, email=email).first()
    else:
        raise ValueError("Either user_id or name and email must be specified")

    if not user:
        raise AuthError("User not found", HTTPStatus.FORBIDDEN)

    return user


def validate_password(password: str, user: User):
    if user.check_password(password):
        return

    raise AuthError("Invalid password", HTTPStatus.FORBIDDEN)


def create_user(password: str, name: str, email: str, role: UserRole):
    try:
        user = User(name=name, email=email, role=role)  # type: ignore
        user.password = password

        db.session.add(user)
        db.session.commit()

        return user
    except SQLAlchemyError as e:
        raise DBException(e)


def validate_role(role: UserRole, API_KEY: Optional[str]):
    match role:
        case UserRole.PATIENT:
            pass
        case UserRole.DOCTOR:
            if API_KEY is None:
                raise AuthError(
                    "You need to give API_KEY to create a doctor", HTTPStatus.FORBIDDEN
                )

            if API_KEY != current_app.config.get("API_KEY"):
                raise AuthError("Your API key is incorrect", HTTPStatus.UNAUTHORIZED)

        case _:
            raise ValueError("Your role is invalid")


def get_role(user_id: int) -> UserRole:
    user = get_user(user_id)

    return user.role
