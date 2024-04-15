from flask import Flask, request
from get_files import get_user_files
from files_to_queue import files_to_queue
from db_service import DBService
import requests
import json
import http
import os
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

auth_url = os.environ.get('AUTH_URL') # 'http://localhost:8081'

# Routes 
@server.route('/health', methods=['GET'])
def health_check():
    return 'OK', http.HTTPStatus.OK

@server.route('/start', methods=['POST'])
def start():
    token = request.headers.get('Authorization')
    if not token:
        return 'Unauthorized', http.HTTPStatus.UNAUTHORIZED
    
    try:
        # Validate token and get gd credentials 
        response = requests.get(f'http://{auth_url}/google/credentials', headers={'Authorization': token})
        if response.status_code != 200:
            return 'Unauthorized from auth service', http.HTTPStatus.UNAUTHORIZED
    except Exception as e:
        print(e)
        return 'Unauthorized from auth service', http.HTTPStatus.UNAUTHORIZED

    gd_credentials = response.json()
    gd_token = gd_credentials.get('gd_token')
    gd_refresh_token = gd_credentials.get('gd_refresh_token')
    user_id = gd_credentials.get('user_id')
    if not gd_token or not gd_refresh_token:
        return 'User has no google credentials', http.HTTPStatus.NOT_FOUND
    
    # get the user's last classification request.
    db_service = DBService()
    last_request = db_service.get_last_classification_request(user_id)

    # if the user has a classification request in progress, return an error
    if last_request and last_request.get('status') != 'done':
        return 'User already has a classification request', http.HTTPStatus.CONFLICT    

    documents = get_user_files(gd_token, gd_refresh_token)

    if(len(documents) == 0):
        return 'No documents found', http.HTTPStatus.NOT_FOUND

    # create classification request
    classification_request = db_service.create_classification_request(user_id, len(documents))
    classification_request_id = str(classification_request.get('_id'))

    files_to_queue(documents, user_id, classification_request_id)

    return "OK", 200

if __name__ == '__main__':
    server.run(host='0.0.0.0')