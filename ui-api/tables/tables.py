from .components import get_documents_data, get_user_data
from db_service import DBService

def get_user_table_data(table, decoded_token):
    try:
         # get user id by email using the decoded token
        db_service = DBService()
        user = db_service.get_user_by_email(decoded_token['email'])
        if(user is None):
            raise Exception('User not found')
        user_id = user['_id']
        if table == 'documents':
            return get_documents_data(user_id)
        elif table == 'users':
            return get_user_data(user)
        else:
            raise Exception('Table not found')
    except Exception as e:
        raise e