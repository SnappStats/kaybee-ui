import json
import os
import secrets
import toml
import dotenv 
from google.cloud import secretmanager

dotenv.load_dotenv()

client = secretmanager.SecretManagerServiceClient()

def main():
    response = client.access_secret_version(
            request={"name": os.environ['OAUTH_SECRET_NAME']})

    secret_data = json.loads(response.payload.data.decode('utf-8'))

    secret_data = {
        'auth': {
            'redirect_uri': os.environ['OAUTH_REDIRECT_URI'],
            'cookie_secret': secrets.token_hex(),
            'google': {
                'client_id': secret_data['web']['client_id'],
                'client_secret': secret_data['web']['client_secret'],
                'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration'
            }
        }
    }

    with open("app/.streamlit/secrets.toml", "w") as f:
        toml.dump(secret_data, f)
