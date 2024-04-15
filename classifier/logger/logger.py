from db_service import DBService
from google_drive_service import update_document_metadata

def create_file_logs(data, classification_vector):
    user_id = data.get('user_id')
    request_id = data.get('request_id')
    metadata = data.get('metadata')
    doc_id = data.get('doc_id')
    top = data.get('top')

    # Find the request by id and update classified_documents and status
    db_service = DBService()
    request = db_service.get_classification_request_by_id(request_id)
    if(not request):
        return False
    request['classified_documents'] = request['classified_documents'] + 1

    if(request['classified_documents'] == 1):
        request['status'] = 'in_progress'

    if(request['classified_documents'] == request['total_documents']):
        request['status'] = 'completed'
    
    db_service.update_classification_request(request.get('_id'), request)

    labels_dic = request.get('labels') # ['Confidential', 'Public', 'Restrictive', 'Internal']
    labels_vector = {}

    for i, label in enumerate(labels_dic):
        try:
            labels_vector[label] = classification_vector[i]
        except IndexError:
            labels_vector[label] = 0

    # Get the label of the highest value of vector
    label = max(labels_vector, key=labels_vector.get)

    # Find if there is file with the same doc_id
    file_id = ''
    file = db_service.get_file_by_doc_id(doc_id)
    if(not file):
        file = db_service.create_file(doc_id, metadata.get('name'), metadata, label, user_id)
        file_id = file.inserted_id
    else:
        db_service.update_file(file.get('_id'), {'label': label})
        file_id = file.get('_id')
    
    # Get the user google drive credentials
    credentials = db_service.get_user_credentials(user_id)

    # Update the metadata of the document
    update_document_metadata(doc_id, label, credentials.get('gd_token'), credentials.get('gd_refresh_token'))

    # Create the file log
    db_service.create_file_classification_log(file_id, request_id, label, top, labels_vector)

    return True
    