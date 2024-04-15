from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

def authenticate(gd_token, gd_refresh_token):
    credentials = Credentials(
        token = gd_token,
        refresh_token = gd_refresh_token,
        token_uri = "https://oauth2.googleapis.com/token",
        client_id = client_id,
        client_secret = client_secret
    )

    return credentials

def update_document_metadata(doc_id, label, gd_token, gd_refresh_token):
    credentials = authenticate(gd_token, gd_refresh_token)
    service = build('drive', 'v3', credentials=credentials)
    # Obtiene el archivo
    file = service.files().get(fileId=doc_id).execute()

    # Etiqueta que deseas agregar al archivo como propiedad
    label_property_key = 'label'
    label_property_value = label
    # Define el cuerpo de la actualización parcial
    partial_update_body = {
        'properties': {
            label_property_key: label_property_value
        }
    }
    # Actualiza parcialmente el archivo con las nuevas propiedades de la aplicación
    updated_file = service.files().update(fileId=doc_id, body=partial_update_body).execute()

    print(updated_file)
    
    return True