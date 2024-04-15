from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import certifi
import time
import os

connectionUrl = os.environ.get('MONGO_URL')
dbName = os.environ.get('MONGO_DB_NAME')
ca = certifi.where()

class DBService:
    def __init__(self):
        self.connectionUrl = connectionUrl
        self.dbName = dbName
        self.ca = ca
        self.db, self.client = self.db_connection()

    def __del__(self):
        self.client.close()

    def db_connection(self):
        try:
            client = MongoClient(self.connectionUrl, tlsCAFile=self.ca, server_api=ServerApi('1'))
            db = client[dbName]
        except ConnectionError as e:
            print(e)
        return db, client

    def get_file_by_doc_id(self, doc_id):
        collection = self.db['files']
        file = collection.find_one({'doc_id': doc_id})
        return file
    
    def create_file(self, doc_id, name, metadata, label, user_id):
        file = {
            'doc_id': doc_id,
            'name': name,
            'user_id': ObjectId(user_id),
            'metadata': metadata,
            'label': label,
            'created_at': int(time.time()),
            'updated_at': int(time.time()),
        }
        collection = self.db['files']
        return collection.insert_one(file)

    def update_file(self, file_id, file):
        collection = self.db['files']
        file['updated_at'] = int(time.time())
        return collection.update_one({'_id': ObjectId(file_id)}, {'$set': file})

    def create_file_classification_log(self, file_id, request_id, label, top, classification_vector):
        collection = self.db['files_logs']
        log = {
            'file_id': ObjectId(file_id),
            'request_id': ObjectId(request_id),
            'classification_vector': classification_vector,
            'label': label,
            'top_lists': top,
            'created_at': int(time.time()),
        }
        return collection.insert_one(log)

    def get_classification_request_by_id(self, req_id):
        collection = self.db['requests']
        request = collection.find_one({'_id': ObjectId(req_id)})
        return request

    def update_classification_request(self, request_id, request):
        collection = self.db['requests']
        request['updated_at'] = int(time.time())
        return collection.update_one({'_id': ObjectId(request_id)}, {'$set': request})
    
    def get_user_credentials(self, user_id):
        collection = self.db['credentials']
        user = collection.find_one({'user_id': ObjectId(user_id)})
        return user
    
    