from flask import Flask, request
from flask_cors import CORS
import http
from dashboard import get_dashboard_metrics
from auth import decode_token
from tables import get_user_table_data

server = Flask(__name__)
CORS(server)

# Routes
@server.route('/health', methods=['GET'])
def health_check():
    return 'OK', http.HTTPStatus.OK

@server.route('/dashboard/<string:section>', methods=['GET'])
def dashboard_metrics(section):
    try: 
        token = request.headers.get('Authorization')
        if not token:
            return 'Unauthorized', http.HTTPStatus.UNAUTHORIZED
        
        token= token.split(' ')[-1]
        decoded_token = decode_token(token)
        data = get_dashboard_metrics(section, decoded_token)
        response = {
            section: data
        }
        return response, http.HTTPStatus.OK
    except Exception as e:
        return str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

@server.route('/table/<string:table>', methods=['GET'])
def get_table_data(table):
    try: 
        token = request.headers.get('Authorization')
        if not token:
            return 'Unauthorized', http.HTTPStatus.UNAUTHORIZED
        
        token= token.split(' ')[-1]
        decoded_token = decode_token(token)
        data = get_user_table_data(table, decoded_token)
        response = {
            table: data
        }
        return response, http.HTTPStatus.OK
    except Exception as e:
        return str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True, port=8080)