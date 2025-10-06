import threading
import requests
import os

def ping_self():
    """
    Periodically sends a GET request to the app's own Render URL
    to prevent Render's free-tier instance from going idle.
    """
    url = os.getenv("RENDER_URL")  # Set this in Render environment variables
    if not url:
        print("No RENDER_URL set. Skipping self-ping.")
        return

    try:
        requests.get(url)
        print(f"✅ Self-ping sent to {url}")
    except Exception as e:
        print(f"⚠️ Self-ping failed: {e}")

    # Schedule the next ping after 14 minutes
    threading.Timer(14 * 60, ping_self).start()

def start_keep_alive():
    """
    Starts the background keep-alive ping process.
    """
    print("🚀 Starting keep-alive service...")
    ping_self()
