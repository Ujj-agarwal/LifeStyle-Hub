import requests
import json
from flask import current_app

def get_gemini_key():
    """
    Safely retrieves the Gemini API key either from current_app (inside a Flask context)
    or directly from the config file (outside request context).
    """
    try:
        api_key = current_app.config.get('GEMINI_API_KEY')
    except RuntimeError:
        # current_app not active (e.g., called outside Flask route)
        from config import Config
        api_key = Config.GEMINI_API_KEY
    return api_key


def call_gemini_api(prompt):
    """Calls the Gemini API with better error handling and visibility."""
    api_key = get_gemini_key()

    if not api_key or not api_key.startswith("AIza"):
        raise ValueError("Gemini API key is not configured in config.py.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # 👇 handle Gemini errors clearly
        if "error" in data:
            err = data["error"]
            raise RuntimeError(f"Gemini API error: {err.get('message', 'Unknown error')}")

        # 👇 safer parsing (some responses use 'candidates' differently)
        candidates = data.get("candidates")
        if not candidates:
            print("Unexpected Gemini response:", data)
            raise RuntimeError("No valid candidates returned from Gemini API.")

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts or "text" not in parts[0]:
            print("Malformed Gemini response:", data)
            raise RuntimeError("Gemini response missing expected text.")

        return parts[0]["text"].strip()

    except requests.RequestException as e:
        print("Request error:", e)
        raise RuntimeError("Network or connection error with Gemini API.")
    except Exception as e:
        print("Gemini API call failed:", e)
        raise RuntimeError(str(e))



def generate_workout_suggestion(workout_type, user_history):
    """Generates a workout suggestion based on user history."""
    history_str = ", ".join(
        [f"{w.workout_type.name} ({w.duration_minutes} mins)" for w in user_history[-5:]]
    )
    prompt = f"""
    As a fitness coach, suggest a simple 3-4 exercise workout for a '{workout_type}' session.
    The user's recent workouts are: {history_str}.
    Please provide the response as a minified JSON object with keys:
    "title" (string), "exercises" (an array of objects with "name" and "details" strings), and "notes" (string).
    Example: {{"title":"Strength Workout","exercises":[{{"name":"Squats","details":"3 sets of 10"}},...],"notes":"Focus on form."}}
    """
    response_text = call_gemini_api(prompt)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"title": "Workout Plan", "exercises": [], "notes": response_text}


def generate_shopping_list(ingredients):
    """Generates a shopping list from a recipe's ingredients."""
    prompt = f"Format the following ingredients into a simple, categorized shopping list with weights or volumes: {ingredients}. Respond in plain text."
    return call_gemini_api(prompt)


def calculate_recipe_calories(recipe_name, ingredients):
    """Estimates calories for a recipe."""
    prompt = f"Estimate the total calories for a recipe named '{recipe_name}' with these ingredients: {ingredients}. Provide only the estimated number and a brief note, like 'Approx. 450 calories per serving'."
    return call_gemini_api(prompt)


def calculate_workout_calories(workout_type, duration_minutes, intensity):
    """Estimates calories burned during a workout using AI."""
    prompt = f"Estimate the calories burned for a '{workout_type}' workout lasting {duration_minutes} minutes with an intensity level of {intensity} out of 5. Provide only an integer number as the result."
    response_text = call_gemini_api(prompt)
    try:
        return int(''.join(filter(str.isdigit, response_text)))
    except (ValueError, TypeError):
        # Fallback to a basic formula if AI response is not a valid number
        return round(duration_minutes * intensity * 3.5)
