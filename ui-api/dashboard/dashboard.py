from .sections import get_stats_data, get_app_accuracy, get_documents_distribution, get_documents_type
from db_service import DBService

def get_dashboard_metrics(section, decoded_token):
    try:
        # get user id by email using the decoded token
        db_service = DBService()
        user = db_service.get_user_by_email(decoded_token['email'])
        if(user is None):
            raise Exception('User not found')
        user_id = user['_id']
        if section == 'stats':
            return get_stats_data(user_id)
        if section == 'accuracy':
            return get_app_accuracy()
        if section == 'distribution':
            return get_documents_distribution(user_id)
        if section == 'documents_type':
            return get_documents_type(user_id)
        else:
            raise Exception('Invalid section')
    except Exception as e:
        raise e