from db_service import DBService

def get_stats_data(user_id):
    db_service = DBService()
    stats_data = {
        'total_docs': db_service.get_total_docs(user_id),
        'scanned_docs': db_service.get_scanned_docs(user_id),
        'sensitive_data': db_service.get_sensitive_data(user_id),
        'users': db_service.get_total_users()
    }

    return stats_data