from db_service import DBService

def get_user_data(user):
    db_service = DBService()
    users = db_service.get_all_users()
    results = []
    for user in users:
        user_documents_distribution = db_service.get_documents_distribution(user['_id'])
        user_data = {
            'name': user['name'],
        }
        for item in user_documents_distribution:
            key = item['_id']
            value = item['count']
            user_data[key] = value

        risk = db_service.get_sensitive_data(user['_id']) * 60
        user_data['risk'] = '$ ' + str(risk)
        results.append(user_data)

    return results