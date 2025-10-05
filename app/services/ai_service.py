import requests
import json
from flask import current_app
from app.models.workout import Workout, WorkoutType
from typing import List

def generate_workout_suggestion(workout_type: WorkoutType, user_history: List[Workout]) -> dict:
   
    api_key = current_app.config.get('GEMINI_API_KEY')

    # Fallback message if the API key hasn't been configured in config.py
    if not api_key or api_key == 'AIzaSyD9PVTUkKPvV8ctqEyVFMNY8f0UVWzZGOY':
        return {
            "title": "API Key Not Configured",
            "exercises": [{"name": "Please add your Gemini API key to config.py", "details": ""}],
            "notes": "You can obtain a free key from Google AI Studio."
        }

    # Construct a detailed prompt, providing context and specifying the desired JSON output format.
    # This is a key part of "prompt engineering".
    history_summary = f"The user has recently completed {len(user_history)} workouts."
    if user_history:
        # Get the most recent workout for context
        last_workout = user_history[-1]
        history_summary += f" Their last session was a '{last_workout.workout_type.value}' workout."
    
    prompt = (
        f"You are a helpful fitness assistant. Based on the following information, suggest a new '{workout_type.value}' workout. "
        f"The user's recent history: {history_summary}. "
        "Provide 3-4 exercises. "
        "Your entire response MUST be a single, minified JSON object with three keys: "
        "'title' (string), 'exercises' (a list of objects, where each object has 'name' and 'details' strings), "
        "and 'notes' (a string)."
    )

    print("--- SENDING PROMPT TO GEMINI API ---")
    print(prompt)
    print("------------------------------------")
    
    # Gemini API endpoint for the gemini-pro model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        # Make the POST request to the API with a timeout
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)

        response_json = response.json()
        
        # Navigate through the API response structure to find the text content
        candidate = response_json.get('candidates', [{}])[0]
        content = candidate.get('content', {}).get('parts', [{}])[0]
        json_text = content.get('text', '{}')
        
        # The AI's response is a JSON string, so we need to parse it into a Python dictionary
        suggestion = json.loads(json_text)
        
        return suggestion

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return {"title": "Error", "exercises": [], "notes": "Could not connect to the AI service. Please check your network connection."}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing Gemini API response: {e}")
        # This can happen if the AI doesn't return valid JSON
        return {"title": "Error", "exercises": [], "notes": "Received an invalid or unexpected response from the AI service."}

