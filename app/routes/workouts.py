from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.workout import Workout, WorkoutType

workouts_bp = Blueprint('workouts', __name__)

@workouts_bp.route('', methods=['POST'])
@jwt_required()
def create_workout():
    """Create a new workout for the logged-in user."""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['workout_type', 'duration_minutes', 'intensity']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        workout_type_enum = WorkoutType[data['workout_type'].upper()]
    except KeyError:
        return jsonify({"msg": f"Invalid workout_type. Must be one of: {[t.name for t in WorkoutType]}"}), 400

    new_workout = Workout(
        user_id=current_user_id,
        notes=data.get('notes'),
        workout_type=workout_type_enum,
        goal_achieved=data.get('goal_achieved', False),
        duration_minutes=data['duration_minutes'],
        intensity=data['intensity']
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(new_workout.to_dict()), 201

@workouts_bp.route('', methods=['GET'])
@jwt_required()
def get_workouts():
    """Get a paginated and filtered list of workouts for the logged-in user."""
    current_user_id = get_jwt_identity()
    query = Workout.query.filter_by(user_id=current_user_id)

    # Filtering by workout type
    workout_type_filter = request.args.get('workout_type')
    if workout_type_filter:
        try:
            query = query.filter_by(workout_type=WorkoutType[workout_type_filter.upper()])
        except KeyError:
            pass # Ignore invalid filter values

    # Bonus: Search within notes
    search_term = request.args.get('q')
    if search_term:
        query = query.filter(Workout.notes.ilike(f'%{search_term}%'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_workouts = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "workouts": [w.to_dict() for w in paginated_workouts.items],
        "total": paginated_workouts.total,
        "pages": paginated_workouts.pages,
        "current_page": paginated_workouts.page
    }), 200

@workouts_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    """Get a single workout by its ID."""
    current_user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user_id).first_or_404()
    return jsonify(workout.to_dict()), 200

@workouts_bp.route('/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout(workout_id):
    """Update an existing workout."""
    current_user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user_id).first_or_404()
    data = request.get_json()

    workout.notes = data.get('notes', workout.notes)
    workout.goal_achieved = data.get('goal_achieved', workout.goal_achieved)
    workout.duration_minutes = data.get('duration_minutes', workout.duration_minutes)
    workout.intensity = data.get('intensity', workout.intensity)
    if 'workout_type' in data:
        try:
            workout.workout_type = WorkoutType[data['workout_type'].upper()]
        except KeyError:
            return jsonify({"msg": "Invalid workout_type"}), 400

    db.session.commit()
    return jsonify(workout.to_dict()), 200

@workouts_bp.route('/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    """Delete a workout."""
    current_user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user_id).first_or_404()
    
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"msg": "Workout deleted successfully"}), 200

@workouts_bp.route('/test-auth', methods=['GET'])
@jwt_required()
def test_auth():
    """A simple endpoint to check if the JWT token is valid."""
    current_user_id = get_jwt_identity()
    return jsonify(message=f"Token is valid! You are user {current_user_id}"), 200