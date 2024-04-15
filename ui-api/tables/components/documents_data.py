from db_service import DBService
from datetime import datetime
from bson import json_util

def get_documents_data(user_id):
    db_service = DBService()
    user_documents = db_service.get_user_documents(user_id)
    results = []
    for doc in user_documents:
        doc_data = {
            'id': str(doc['_id']),
            'file_name': doc['name'],
            'user': doc['metadata']['owners'][0]['displayName'],
            "department":"IT",
            'label': doc['label'],
            'creationDate': datetime.fromtimestamp(doc['created_at']).strftime('%d/%m/%Y'),
            'classificationDate': datetime.fromtimestamp(doc['file_logs'][0]['created_at']).strftime('%d/%m/%Y'),
            'file_logs': json_util.dumps(doc['file_logs'])
        }
        results.append(doc_data)
    return results