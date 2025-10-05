import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration settings for the Flask application.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_very_secret_key'
    
    # Secret key for Flask-JWT-Extended
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another_super_secret_key'

    # ✅ Gemini API key (set directly here)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AIzaSyD9PVTUkKPvV8ctqEyVFMNY8f0UVWzZGOY'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'project.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
