from models import User
from common.exceptions import AuthError, DBException
from http import HTTPStatus
from db import db
from sqlalchemy.exc import SQLAlchemyError

def get_user(user_id: int) -> User:
    user = User.query.get(user_id)
    
    if not user:
        raise AuthError('User not found', HTTPStatus.FORBIDDEN)
    
    return user

def validate_password(password: str, user: User):
    if user.check_password(password):
        return
    
    raise AuthError('Invalid password', HTTPStatus.FORBIDDEN)

def create_user(password: str, name: str, email: str):
    try:
        user = User(name=name, email=email)
        user.password = password
        
        db.session.add(user)
        db.session.commit()
        
        return user
    except SQLAlchemyError as e:
        raise DBException(e)
    