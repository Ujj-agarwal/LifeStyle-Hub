import os
from flask import Flask
from config import Config
from .extensions import db, bcrypt, jwt
from flask_cors import CORS  # <-- Import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Initialize CORS ---
    # For testing: allow all origins
    CORS(app, origins=["https://life-style-hub-qqvj.vercel.app/"])

    # For production: restrict to your Vercel frontend URL
    # CORS(app, origins=["https://your-vercel-app.vercel.app"])
    # ------------------------

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.workouts import workouts_bp
    from .routes.recipes import recipes_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')

    with app.app_context():
        db.create_all()

    return app
