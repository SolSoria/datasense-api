from db_service import DBService

def get_documents_distribution(user_id):
    db_service = DBService()
    distribution = db_service.get_documents_distribution(user_id)
    return distribution