from config import Config
from flask import Flask
from db import db, ma
from flask_migrate import Migrate
from bcrypt_ext import bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    
    CORS(app)
    
    db.init_app(app)
    Migrate(app, db)
    ma.init_app(app)
    
    bcrypt.init_app(app)
    JWTManager(app)
    
    return app