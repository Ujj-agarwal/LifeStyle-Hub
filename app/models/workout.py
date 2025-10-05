import enum
from app import db

class WorkoutType(enum.Enum):
    STRENGTH = "Strength"
    CARDIO = "Cardio"
    YOGA = "Yoga"

class Workout(db.Model):
    """
    Workout model for storing workout session details.
    """
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text, nullable=True)
    workout_type = db.Column(db.Enum(WorkoutType), nullable=False)
    goal_achieved = db.Column(db.Boolean, default=False, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Integer, nullable=False)  # Scale: 1–5
    
    # Foreign key to link a workout to a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @property
    def calories_burned(self):
        """Calculate calories burned: duration × intensity × type factor."""
        if self.duration_minutes is None or self.intensity is None:
            return 0

        type_factor = {
            "Strength": 6.0,
            "Cardio": 8.0,
            "Yoga": 4.0
        }.get(self.workout_type.value, 5.0)  # default factor if unknown

        calories = self.duration_minutes * self.intensity * type_factor
        return round(calories)

    def to_dict(self):
        """Helper function to serialize the object to a dictionary."""
        return {
            'id': self.id,
            'notes': self.notes,
            'workout_type': self.workout_type.value,
            'goal_achieved': self.goal_achieved,
            'duration_minutes': self.duration_minutes,
            'intensity': self.intensity,
            'calories_burned': self.calories_burned,
            'user_id': self.user_id
        }
