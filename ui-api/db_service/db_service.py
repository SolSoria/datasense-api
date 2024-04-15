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

    def get_user_by_email(self, email):
        collection = self.db['users']
        user = collection.find_one({'email': email})
        return user

    def get_file_by_doc_id(self, doc_id):
        collection = self.db['files']
        file = collection.find_one({'doc_id': doc_id})
        return file

    def get_total_docs(self, user_id):
        collection = self.db['requests']
        request = collection.find_one({'user_id': ObjectId(user_id)}, sort=[('_id', -1)])
        if request is None:
            return 0
        
        total_docs = request['total_documents']
        return total_docs

    def get_scanned_docs(self, user_id):
        collection = self.db['files']
        scanned_docs = collection.count_documents({'user_id': ObjectId(user_id)})
        return scanned_docs

    def get_sensitive_data(self, user_id):
        collection = self.db['files']
        sensitive_labels = ['Restrictive', 'Internal']
        sensitive_docs = collection.count_documents({'user_id': ObjectId(user_id), 'label': {'$in': sensitive_labels}})
        return sensitive_docs
    
    def get_total_users(self):
        collection = self.db['users']
        total_users = collection.count_documents({})
        return total_users

    def get_documents_distribution(self, user_id):
        collection = self.db['files']
        distribution = collection.aggregate([
            {'$match': {'user_id': ObjectId(user_id)}},
            {'$group': {'_id': '$label', 'count': {'$sum': 1}}}
        ])
        return list(distribution)

    def get_documents_types(self, user_id):
        collection = self.db['files']
        distribution = collection.aggregate([
            {'$match': {'user_id': ObjectId(user_id)}},
            {'$group': {'_id': '$metadata.mimeType', 'count': {'$sum': 1}}}
        ])
        return list(distribution)
    
    def get_user_last_request(self, user_id):
        collection = self.db['requests']
        request = collection.find_one({'user_id': ObjectId(user_id)}, sort=[('_id', -1)])
        return request

    def get_all_users(self):
        collection = self.db['users']
        users = collection.find({})
        return list(users)

    def get_user_documents(self, user_id):
        collection = self.db['files']
        pipeline = [
            {'$match': {'user_id': ObjectId(user_id)}},
            {'$lookup': {
                'from': 'files_logs',
                'let': {'file_id': '$_id'},
                'pipeline': [
                    {'$match': {'$expr': {'$eq': ['$file_id', '$$file_id']}}},
                    {'$sort': {'_id': -1}},
                    {'$limit': 1},
                    {'$project': {
                        'classification_vector': 1,
                        'label': 1,
                        'created_at': 1,
                        'top_lists': 1
                    }}
                ],
                'as': 'file_logs'
            }}
        ]
        user_documents = collection.aggregate(pipeline)
        return list(user_documents)