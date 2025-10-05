from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration route.
    Expects a JSON payload with 'username' and 'password'.
    """
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({"msg": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409 # 409 Conflict

    # Create a new user and set the password
    new_user = User(username=username)
    new_user.set_password(password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login route.
    Expects 'username' and 'password'. Returns a JWT access token on success.
    """
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({"msg": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    # Find the user by username
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and user.check_password(password):
        # Create a JWT token for the user
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401 # 401 Unauthorized
