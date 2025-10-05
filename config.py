import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration settings for the Flask application.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_very_secret_key'
    
    # Secret key for Flask-JWT-Extended is crucial for token security
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another_super_secret_key'

    # Corrected database path to create the db inside the instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'project.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
