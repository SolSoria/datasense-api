from flask import Flask, request
from google_service import get_google_drive_tokens, get_user_info
from auth_service import decode_token, AuthService
from flask_cors import CORS
import http

server = Flask(__name__)
CORS(server)

# Routes 
@server.route('/health', methods=['GET'])
def health_check():
    return 'OK', http.HTTPStatus.OK

@server.route('/login/google', methods=['POST'])
def login_google():
    code = request.json.get('code')
    gd_token, gd_refresh_token, id_token = get_google_drive_tokens(code)
    if not gd_token or not gd_refresh_token or not id_token:
        return 'Invalid code', http.HTTPStatus.UNAUTHORIZED
    email, name, picture, google_id = get_user_info(id_token)
    auth_service = AuthService()
    token = auth_service.get_user_token(name, email, picture, google_id, gd_token, gd_refresh_token)
    return {
        "token": token
    }, http.HTTPStatus.OK

@server.route('/token/validate', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization')
    # Delete Bearer from token
    token = token.split(' ')[-1]
    if not token:
        return 'Unauthorized', 401

    decoded_token = decode_token(token)
    return decoded_token, http.HTTPStatus.OK

@server.route('/google/credentials', methods=['GET'])
def get_google_credentials():
    token = request.headers.get('Authorization')
    # Delete Bearer from token
    token = token.split(' ')[-1]
    if not token:
        return 'Unauthorized', http.HTTPStatus.UNAUTHORIZED

    decoded_token = decode_token(token)
    user_id = str(decoded_token.get('user_id'))
    auth_service = AuthService()
    credentials = auth_service.get_user_google_drive_credentials(user_id)
    return {
        "user_id": str(credentials.get('user_id')),
        "gd_token": credentials.get('gd_token'),
        "gd_refresh_token": credentials.get('gd_refresh_token')
    }, http.HTTPStatus.OK

@server.route('/google/credentials/<string:user_id>', methods=['GET'])
def get_google_credentials_by_id(user_id):
    if not user_id:
        return 'No user id', http.HTTPStatus.BAD_REQUEST

    auth_service = AuthService()
    credentials = auth_service.get_user_google_drive_credentials(user_id)
    return {
        "gd_token": credentials.get('gd_token'),
        "gd_refresh_token": credentials.get('gd_refresh_token')
    }, http.HTTPStatus.OK

if __name__ == '__main__':
    server.run(host='0.0.0.0')