"""Explicit browser authorization CLI. Never invoked by an MCP tool."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from drive_api import BASE, SCOPES, load_environment, save_private

if __name__ == '__main__':
    load_environment()
    config = {'installed': {'client_id': os.environ['GOOGLE_CLIENT_ID'],
                           'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
                           'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                           'token_uri': 'https://oauth2.googleapis.com/token'}}
    flow = InstalledAppFlow.from_client_config(config, SCOPES, autogenerate_code_verifier=True)
    credentials = flow.run_local_server(host='127.0.0.1', port=0, access_type='offline', prompt='consent',
                                       authorization_prompt_message='Open the authorization page in your browser: {url}',
                                       success_message='Authorization finished. Return to your coding agent.')
    save_private(os.environ.get('GOOGLE_TOKEN_PATH', str(BASE / '.private/token.json')), credentials.to_json())
    print('Private authorization cache saved. No token values displayed.')
