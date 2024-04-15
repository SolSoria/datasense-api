from db_service import DBService

documents_type_dict = {
    'text/csv': '.csv',
    'application/pdf': '.pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/vnd.google-apps.presentation': 'others',
    'application/vnd.google-apps.spreadsheet': 'others',
    'application/vnd.google-apps.document': 'others',
}

def get_documents_type(user_id):
    db_service = DBService()
    documents_type = db_service.get_documents_types(user_id)

    # Crear un nuevo diccionario para almacenar los resultados
    result = {
        ".pdf": 0,
        ".docx": 0,
        ".xlsx": 0,
        ".pptx": 0,
        ".csv": 0,
        "others": 0
    }
    for document_type in documents_type:
        # Obtener la extensión del tipo de documento
        extension = documents_type_dict.get(document_type['_id'], 'others')
        # Si la extensión es 'others', sumar el conteo al valor existente
        if extension == 'others':
            result[extension] = result.get(extension, 0) + document_type['count']
        else:
            result[extension] = document_type['count']
    return result