import jwt
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ.get('SECRET_KEY')

def decode_token(token):
    return jwt.decode(token, secret_key, algorithms=['HS256'])