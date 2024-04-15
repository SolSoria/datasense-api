from google.oauth2.credentials import Credentials
from google_drive_downloader import download_file
from googleapiclient.discovery import build
from google.cloud import pubsub_v1
from text_extractor import text_extractor
import requests
import os
import json
import time
import sys

client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
project_id = os.environ.get("PROJECT_ID") # dev-gd-classifier-v1
subscription_id = os.environ.get("SUBSCRIPTION_ID") # files-to-download-sub
files_to_classify_topic_id = os.environ.get('FILES_TO_CLASSIFY_TOPIC_ID') # files-to-classify
credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH') # pubsub/credentials.json
credentials_path = os.path.join(os.path.dirname(__file__), credentials_file_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

auth_url = os.environ.get('AUTH_URL') # 'http://localhost:8081'
vectorizer_url = os.environ.get('VECTORIZER_URL') # 'http://localhost:8083'

token_uri = 'https://oauth2.googleapis.com/token'

def authenticate(gd_token, gd_refresh_token):
    credentials = Credentials(
        token=gd_token,
        refresh_token=gd_refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri=token_uri,
    )
    # Refrescar las credenciales si es necesario
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    return credentials

def get_user_gd_credentials(user_id):
    try:
        # Validate token and get gd credentials 
        response = requests.get(f'http://{auth_url}/google/credentials/{user_id}')
        if response.status_code != 200:
            return None
    except Exception as e:
        print(e)
        return None
    
    return response.json()

def get_vectors(content, user_id):
    try:
        response = requests.post(f'http://{vectorizer_url}/vectorize', json={
            "content": f"{content}",
            "user_id": user_id
        })
        if response.status_code != 200:
            return None
    except Exception as e:
        print(e)
        sys.stdout.flush()
        return None
    
    return response.json()

def files_to_queue(message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, files_to_classify_topic_id)
    message = json.dumps(message).encode('utf-8')
    future = publisher.publish(topic_path, data=message)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()

    print(f"Published messages to {topic_path}.")
    sys.stdout.flush()
    return

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # timeout = 5.0

    def callback(message):
        data = json.loads(message.data)
        user_id = data['user_id'];
        gd_credentials = get_user_gd_credentials(user_id)
        if(not gd_credentials):
            print(f'User {user_id} has no google credentials')
            sys.stdout.flush()
            message.ack()
            return
        try:
            credentials = authenticate(gd_credentials.get('gd_token'), gd_credentials.get('gd_refresh_token'))
            service = build('drive', 'v3', credentials=credentials)
            download_file_name, file_metadata = download_file(data['doc_id'], service=service)
            ## transform the file to pdf and extract the content
            content = text_extractor(download_file_name)
            ## Hard delete the document
            # Check if the file exists and delete it
            if os.path.isfile(download_file_name):
                os.remove(download_file_name)
            else:
                print(f"Error: {download_file_name} not found")
                sys.stdout.flush()
            ## Call the vectorizer service. Send the file data, user_id and request_id
            vectors = get_vectors(content, user_id)
                
            message_classify = {
                "vector": vectors.get('tfidf_vector'),
                "top": vectors.get('top'),
                "user_id": user_id,
                "request_id": data['request_id'],
                "metadata": file_metadata,
                "doc_id": data['doc_id'],
            }

            files_to_queue(message_classify)
            # Push the vectorized document into a new pub/sub topic
            message.ack()
            
        except Exception as e:
            print(e)
            sys.stdout.flush()
            message.ack()
            return

    future = subscriber.subscribe(subscription_path, callback)
    print("Listening for messages on {}".format(subscription_path))
    sys.stdout.flush()

    with subscriber as subscriber:
        try:
            future.result()
        except TimeoutError:
            future.cancel()
            print(f"TimeoutError: {future.exception()}")

if __name__ == '__main__':
    main()