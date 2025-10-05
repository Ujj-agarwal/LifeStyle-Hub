import os

class Config:
    """
    Configuration class for the Flask application.
    It's best practice to load sensitive information from environment variables.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key-that-you-should-change')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'another-super-secret-jwt-key')
    
    # Configure the database URI. For this example, we'll use a simple SQLite database.
    # For a production application, you would use something like PostgreSQL or MySQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
