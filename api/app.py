from config import Config
from flask import Flask
from db import db, ma
from flask_migrate import Migrate
from bcrypt_ext import bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from error_handler.controller import error_bp
from auth.controller import auth_bp
from management.controller import management_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    Migrate(app, db)
    ma.init_app(app)

    bcrypt.init_app(app)
    JWTManager(app)

    app.register_blueprint(error_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(management_bp, url_prefix="/api/management")

    return app
