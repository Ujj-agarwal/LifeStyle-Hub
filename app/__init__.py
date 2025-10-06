import os
from flask import Flask
from config import Config
from .extensions import db, bcrypt, jwt
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Explicit CORS configuration
    CORS(
        app,
        resources={r"/*": {"origins": [
            "http://localhost:3000",                     # Local dev frontend
            "https://life-style-hub-qqvj.vercel.app"    # Deployed frontend origin
        ]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.workouts import workouts_bp
    from .routes.recipes import recipes_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')

    with app.app_context():
        db.create_all()

        from .keep_alive import start_keep_alive
    start_keep_alive()

    return app
