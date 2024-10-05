from db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from bcrypt_ext import bcrypt
from common.constants import UserRole


class User(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: UserRole = db.Column(
        db.Integer,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("name", "email", name="name with email should be unique"),
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.generate_password_hash(value).decode("utf8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
