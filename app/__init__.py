import os
from flask import Flask
from config import Config
# Import extensions from the new central file
from .extensions import db, bcrypt, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the instance folder exists for the database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app instance
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints for all routes
    from .routes.auth import auth_bp
    from .routes.workouts import workouts_bp
    from .routes.recipes import recipes_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')

    with app.app_context():
        # Create database tables for all models upon startup
        db.create_all()

    return app

