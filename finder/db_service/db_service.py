from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import certifi
import time
import os

# connectionUrl = 'mongodb+srv://datasense_dev_usr:a5nRYhpxVSujg6iH@datasense.0p8jnhm.mongodb.net/?retryWrites=true&w=majority&appName=DataSense'
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

    def get_last_classification_request(self, user_id):
        collection = self.db['requests']
        request = collection.find_one({'user_id': ObjectId(user_id)}, sort=[('_id', -1)])
        return request
    
    def create_classification_request(self, user_id, total_documents):
        collection = self.db['requests']
        labels = ['Confidential', 'Public', 'Restrictive', 'Internal']
        request = {
            'user_id': ObjectId(user_id),
            'status': 'pending',
            'total_documents': total_documents,
            'classified_documents': 0,
            'labels': labels,
            'created_at': int(time.time()),
            'updated_at': int(time.time()),
        }
        collection.insert_one(request)
        return request