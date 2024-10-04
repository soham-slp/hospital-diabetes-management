from auth.models import User
from common.exceptions import AuthError, DBException
from http import HTTPStatus
from db import db
from sqlalchemy.exc import SQLAlchemyError
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


def create_user(password: str, name: str, email: str):
    try:
        user = User(name=name, email=email)
        user.password = password

        db.session.add(user)
        db.session.commit()

        return user
    except SQLAlchemyError as e:
        raise DBException(e)
