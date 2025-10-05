from app.extensions import db, bcrypt

class User(db.Model):
    """
    User model for storing user details and handling password security.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Defines the one-to-many relationships
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade="all, delete-orphan")
    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

