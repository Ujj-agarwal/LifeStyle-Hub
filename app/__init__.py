import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the instance folder exists before initializing the database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # The folder already exists, which is fine.
        pass

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.workouts import workouts_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')

    with app.app_context():
        # Create database tables for all models
        db.create_all()

    return app