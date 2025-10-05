from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration route."""
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({"msg": "Missing username or password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login route."""
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        # THE FIX: JWT identity must be a string.
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401