from app.models.workout import Workout, WorkoutType
from typing import List

def generate_workout_suggestion(workout_type: WorkoutType, user_history: List[Workout]) -> dict:
    """
    Simulates a call to an AI model to generate a workout suggestion.

    In a real implementation, this function would:
    1. Construct a detailed prompt including the workout_type and user_history.
    2. Make an API call to an AI service (e.g., Gemini API).
    3. Parse the AI's response and return it in a structured format.

    For this assignment, we return a hardcoded, realistic response.
    """
    
    # Example of how you might use user_history to build a prompt
    history_summary = f"The user has recently completed {len(user_history)} workouts."
    if user_history:
        last_workout = user_history[-1]
        history_summary += f" Their last session was a '{last_workout.workout_type.value}' workout."
    
    prompt = (
        f"Based on the following information, suggest a new '{workout_type.value}' workout. "
        f"The user's recent history: {history_summary}. "
        "Please provide 3-4 exercises with sets and reps."
    )
    
    print("--- SIMULATED AI PROMPT ---")
    print(prompt)
    print("---------------------------")
    
    # Hardcoded AI responses based on workout type
    if workout_type == WorkoutType.STRENGTH:
        suggestion = {
            "title": "Strength Session Suggestion",
            "exercises": [
                {"name": "Barbell Squats", "details": "3 sets of 8-10 reps"},
                {"name": "Bench Press", "details": "3 sets of 8-10 reps"},
                {"name": "Deadlifts", "details": "1 set of 5 reps"},
                {"name": "Overhead Press", "details": "3 sets of 10-12 reps"}
            ],
            "notes": "Focus on proper form. Rest 90 seconds between sets."
        }
    elif workout_type == WorkoutType.CARDIO:
        suggestion = {
            "title": "Cardio Session Suggestion",
            "exercises": [
                {"name": "Warm-up Jog", "details": "5 minutes at a light pace"},
                {"name": "Interval Sprints", "details": "8 rounds of 30 seconds sprint, 60 seconds walk"},
                {"name": "Steady-State Cycling", "details": "20 minutes at a moderate pace"},
                {"name": "Cool-down Walk", "details": "5 minutes"}
            ],
            "notes": "Stay hydrated and monitor your heart rate."
        }
    elif workout_type == WorkoutType.YOGA:
        suggestion = {
            "title": "Yoga Flow Suggestion",
            "exercises": [
                {"name": "Sun Salutation A", "details": "5 rounds"},
                {"name": "Warrior II Pose", "details": "Hold for 5 breaths on each side"},
                {"name": "Triangle Pose", "details": "Hold for 5 breaths on each side"},
                {"name": "Savasana (Corpse Pose)", "details": "5-10 minutes of relaxation"}
            ],
            "notes": "Focus on your breath and move with intention."
        }
    else:
        suggestion = {
            "title": "General Workout Suggestion",
            "exercises": [{"name": "No specific suggestion available", "details": ""}],
            "notes": "Please select a valid workout type."
        }
        
    return suggestion

