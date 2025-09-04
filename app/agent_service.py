import base64
import os
import requests
from dotenv import load_dotenv
from floggit import flog

# Load environment variables from .env file
load_dotenv()

AGENT_URL = os.environ['AGENT_URL']
APP_NAME = os.environ['APP_NAME']

@flog
def get_agent_response(
        user_id: str,
        session_id: str,
        text: str = '',
        files: list = []) -> dict:
    url = f'{AGENT_URL}/run_sse'

    parts = [{"text": text}]
    if files:
        file_bytes = files[0].read()
        encoded_data = base64.b64encode(file_bytes).decode('utf-8')
        parts.append(
            {
                'inlineData': {
                    'displayName': files[0].name,
                    'data': encoded_data,
                    'mimeType': files[0].type
                }
            }
        )

    payload = {
        "app_name": APP_NAME,
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {"parts": parts, "role": "user"},
        'streaming': True
    }
    response = requests.post(url, stream=True, json=payload)
    for asdf in response:
        yield asdf


@flog
def create_session(user_id: str, company: str) -> str:
    url = f'{AGENT_URL}/apps/{APP_NAME}/users/{user_id}/sessions'
    response = requests.post(url, json={"company": company})
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
