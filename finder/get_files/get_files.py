from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

allowed_mimetypes = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.google-apps.presentation',
    'application/vnd.google-apps.spreadsheet',
    'application/vnd.google-apps.document',
    'text/csv',
    'application/pdf'
]

client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

def get_user_files(gd_token, gd_refresh_token):
    # Cargar las credenciales con el token de acceso
    credentials = Credentials(
        token = gd_token,
        refresh_token = gd_refresh_token,
        token_uri = "https://oauth2.googleapis.com/token",
        client_id = client_id,
        client_secret = client_secret
    )
    # Construir la query para buscar los archivos
    query = " or ".join([f"mimeType='{mimetype}'" for mimetype in allowed_mimetypes])
    # Construir el servicio de la API de Google Drive
    service = build('drive', 'v3', credentials=credentials)
    documents = []
    page_token = None
    page = 1
    while True:
        response = service.files().list(
            pageSize=5,
            fields="nextPageToken, files(id, name)",
            q=query,
            pageToken=page_token
        ).execute()
        print(f"Page {page}")
        page += 1
        for file in response.get('files', []):
            # Process change
            documents.append(file)
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    
    print(f"Total files: {len(documents)}")
    return documents
