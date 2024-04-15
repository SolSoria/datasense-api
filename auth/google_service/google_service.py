from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")

def get_google_drive_tokens(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()
    if("error" in tokens):
        return None, None, None
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    id_token = tokens["id_token"]
    return access_token, refresh_token, id_token

def get_user_info(id_token):
    """Get user information from the id token."""

    decoded_token = jwt.decode(id_token, options={"verify_signature": False})  
    email = decoded_token.get("email", "")
    name = decoded_token.get("name", "")
    picture = decoded_token.get("picture", "")
    sub = decoded_token.get("sub", "")
    return email, name, picture, sub
