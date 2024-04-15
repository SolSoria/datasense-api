from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import certifi
import jwt
import os

secret_key = os.environ.get('SECRET_KEY')
connectionUrl = os.environ.get('MONGO_URL')
dbName = os.environ.get('MONGO_DB_NAME')
ca = certifi.where()

class AuthService:
    def __init__(self):
        self.connectionUrl = connectionUrl
        self.dbName = dbName
        self.ca = ca
        self.db, self.client = self.db_connection()

    def __del__(self):
        self.client.close()  # Close database connection when object is destroyed

    def db_connection(self):
        try:
            client = MongoClient(self.connectionUrl, tlsCAFile=self.ca, server_api=ServerApi('1'))
            db = client[dbName]
        except ConnectionError as e:
            print(e)
        return db, client

    def get_user_token(self, name, email, picture, google_id, gd_token, gd_refresh_token):
        user = self.get_user_by_email(email)
        if(not user):
            user = self._create_user_and_credentials(name, email, picture, google_id, gd_token, gd_refresh_token)
        
        self._update_user_credentials(str(user['_id']), gd_token, gd_refresh_token)
        payload = {
            "user_id": str(user['_id']),
            "email": user['email'],
            "name": user['name'],
            "picture": user['google']['picture']
        }

        token = encode_token(payload)
        self.client.close()
        return token

    def get_user_by_email(self, email):
        collection = self.db['users']
        user = collection.find_one({'email': email})
        return user

    def get_user_google_drive_credentials(self, user_id):
        collection = self.db['credentials']
        credentials = collection.find_one({'user_id': ObjectId(user_id)})
        return credentials

    def _update_user_credentials(self, user_id, gd_token, gd_refresh_token):
        collection = self.db['credentials']
        collection.update_one({'user_id': ObjectId(user_id)}, {'$set': {'gd_token': gd_token, 'gd_refresh_token': gd_refresh_token}})
        return True

    def create_user(self, name, email, picture, google_id):
        collection = self.db['users']
        user = {
            'name': name,
            'email': email,
            'google': {
                'id': google_id,
                'picture': picture
            }
        }
        user = collection.insert_one(user)
        return user

    def create_credentials(self, user_id, gd_token, gd_refresh_token):
        collection = self.db['credentials']
        credentials = {
            'user_id': user_id,
            'gd_token': gd_token,
            'gd_refresh_token': gd_refresh_token
        }
        credentials = collection.insert_one(credentials)
        return credentials

    def get_user_by_id(self, user_id):
        collection = self.db['users']
        user = collection.find_one({'_id': ObjectId(user_id)})
        return user

    def _create_user_and_credentials(self, name, email, picture, google_id, gd_token, gd_refresh_token):
        user_created = self.create_user(name, email, picture, google_id)
        user = self.get_user_by_id(user_created.inserted_id)
        credentials = self.create_credentials(user_created.inserted_id, gd_token, gd_refresh_token)
        return user

def encode_token(data):
    return jwt.encode(data, secret_key, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, secret_key, algorithms=['HS256'])
