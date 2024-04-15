from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO

regular_mime_types = [
    'application/pdf', # pdf
    'application/vnd.ms-excel', # xls
    'application/msword', # doc
    'application/vnd.ms-powerpoint', # ppt
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', # docx
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', # xlsx
    'application/vnd.openxmlformats-officedocument.presentationml.presentation', # pptx
    'text/csv',
]

drive_mimetypes = [
    'application/vnd.google-apps.presentation',
    'application/vnd.google-apps.spreadsheet',
    'application/vnd.google-apps.document',
]


def download_drive_file(file_id, service):
    # Descargar el archivo
    request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
    file_handle = BytesIO()
    downloader = MediaIoBaseDownload(file_handle, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    file_handle.seek(0)
    return file_handle

def download_regular_file(file_id, service):
    request = service.files().get_media(fileId=file_id)
    file_handle = BytesIO()
    downloader = MediaIoBaseDownload(file_handle, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    file_handle.seek(0)
    return file_handle

def save_pdf(pdf_output, file_name, file_metadata):
    # Obtener el nombre del archivo y la extensión si es un archivo regular
    if file_metadata['mimeType'] in regular_mime_types:
        extension = file_metadata['name'].split('.')[-1]
        file_name += f".{extension}"
    else:
        file_name += ".pdf"
    # Guardar el PDF en el sistema de archivos
    with open(file_name, 'wb') as f:
        f.write(pdf_output.read())
    
    return file_name

def download_file(file_id, service):

    # Descargar y convertir cada archivo
    file_metadata = service.files().get(fileId=file_id, fields='name,mimeType,createdTime,size,owners').execute()
    mime_type = file_metadata.get('mimeType')
    if mime_type in regular_mime_types:
        file_handle = download_regular_file(file_id, service)
    elif mime_type in drive_mimetypes:
        file_handle = download_drive_file(file_id, service)
    else:
        print(f"MimeType {mime_type} not compatible. File id = {file_id}")
        return

    file_name = save_pdf(file_handle, file_id, file_metadata)
    print(f"Processed file: {file_metadata['name']}")
    # return the file metadata
    metadata = {
        'name': file_metadata['name'],
        'mimeType': file_metadata['mimeType'],
        'size': file_metadata['size'],
        'created_at': file_metadata['createdTime'],
        'owners': file_metadata['owners']
    }
    return file_name, metadata
