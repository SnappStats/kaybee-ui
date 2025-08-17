import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AGENT_URL = os.environ['AGENT_URL']
APP_NAME = os.environ['APP_NAME']

def get_agent_response(
        user_input: str, user_id: str, session_id: str) -> dict:
    url = f'{AGENT_URL}/run'
    payload = {
        "app_name": APP_NAME,
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {
            "parts": [{"text": user_input}],
            "role": "user"
        },
    }
    return requests.post(url, json=payload).json()


def create_session(user_id: str) -> str:
    url = f'{AGENT_URL}/apps/{APP_NAME}/users/{user_id}/sessions'
    response = requests.post(url)
    return response.json()['id']


def stream_agent_response(
        user_input: str, user_id: str, session_id: str) -> dict:
    url = f'{AGENT_URL}/run_sse'
    payload = {
        "appName": APP_NAME,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "parts": [{"text": user_input}],
            "role": "user"
        },
        "streaming": False
    }
    for e in requests.post(url, json=payload):
        yield e
